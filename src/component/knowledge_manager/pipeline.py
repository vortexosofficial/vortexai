import os
import runpy
import toml
import asyncio
from aios import KnowledgePipelineEnvironment, KnowledgePipeline


class KnowledgePipelineManager:
    @classmethod
    def initial(cls, root_dir: str):
        cls._instance = KnowledgePipelineManager(root_dir)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance    
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.input_modules = {}
        self.parser_modules = {}
        self.pipelines = {
            "names": {},
            "running": []
        }

    def register_input(self, name: str, init_method):
        self.input_modules[name] = init_method
        
    def register_parser(self, name: str, parser_method):
        self.parser_modules[name] = parser_method

    def add_pipeline(self, config: dict, path: str):
        name = config["name"]
        if name in self.pipelines["names"]:
            return
        
        input_module = config["input"]["module"]
        _, ext = os.path.splitext(input_module)
        if ext == ".py":
            input_module = os.path.join(path, input_module)
            input_init = runpy.run_path(input_module)["init"]
        else:
            input_init = self.input_modules.get(input_module)
        input_params = config["input"].get("params")

        parser_config = config.get("parser")
        if parser_config is None:
            parser_init = None
            parser_params = None
        else:
            parser_module = parser_config["module"]
            _, ext = os.path.splitext(parser_module)
            if ext == ".py":
                parser_module = os.path.join(path, parser_module)
                parser_init = runpy.run_path(parser_module)["init"]
            else:
                parser_init = self.parser_modules.get(parser_module)
            parser_params = parser_config.get("params")


        data_path = os.path.join(self.root_dir, name)
        env = KnowledgePipelineEnvironment(data_path)
        pipeline = KnowledgePipeline(name, env, input_init, input_params, parser_init, parser_params)
        self.pipelines["names"][name] = pipeline
        self.pipelines["running"].append(pipeline)

    def get_pipelines(self) -> [KnowledgePipeline]:
        return self.pipelines["running"]
    
    def get_pipeline(self, name: str) -> KnowledgePipeline:
        return self.pipelines["names"].get(name)

    async def run(self):
        while True:
            for pipeline in self.pipelines["running"]:
                await pipeline.run()
            await asyncio.sleep(5)

    def load_dir(self, root: str):
        config_path = os.path.join(root, "pipelines.toml")
        if not os.path.exists(config_path):
            return 
        with open(config_path, "r") as f:
            config = toml.load(f)
        for path in config["pipelines"]:
            pipeline_path = os.path.join(root, path)
            with open(os.path.join(pipeline_path, "pipeline.toml"), 'r', encoding='utf-8') as f:
                pipeline_config = toml.load(f)
                self.add_pipeline(pipeline_config, pipeline_path)
