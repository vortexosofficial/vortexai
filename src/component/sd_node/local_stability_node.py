import os
import io
import asyncio
from asyncio import Queue
import logging
import base64
from PIL import Image
import requests
from typing import Tuple
from pathlib import Path

from aios import ComputeTask, ComputeTaskResult, ComputeTaskState, ComputeTaskType,ComputeTaskResultCode,ComputeNode,AIStorage,UserConfig

logger = logging.getLogger(__name__)


class Local_Stability_ComputeNode(ComputeNode):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Local_Stability_ComputeNode()
        return cls._instance

    @classmethod
    def declare_user_config(cls):
        user_config = AIStorage.get_instance().get_user_config()
        if os.getenv("LOCAL_STABILITY_URL") is None:
            user_config.add_user_config(
                "local_stability_url", "local stability url", True, None)
        if os.getenv("TEXT2IMG_OUTPUT_DIR") is None:
            home_dir = Path.home()
            output_dir = Path.joinpath(home_dir, "text2img_output")
            Path.mkdir(output_dir, exist_ok=True)
            user_config.add_user_config(
                "text2img_output_dir", "text2image output dir", True, output_dir)
        if os.getenv("TEXT2IMG_DEFAULT_MODEL") is None:
            user_config.add_user_config(
                "text2img_default_model", "text2img default model", True, "v1-5-pruned-emaonly")

    def __init__(self) -> None:
        super().__init__()

        self.is_start = False
        self.node_id = "local_stability_node"
        self.url = None
        self.default_model = None
        self.output_dir = None

        self.task_queue = Queue()
    
    async def initial(self):
        if os.getenv("LOCAL_STABILITY_URL") is not None:
            self.url = os.getenv("LOCAL_STABILITY_URL")
        else:
            self.url = AIStorage.get_instance(
            ).get_user_config().get_value("local_stability_url")

        if os.getenv("TEXT2IMG_OUTPUT_DIR") is not None:
            self.output_dir = os.getenv("TEXT2IMG_OUTPUT_DIR")
        else:
            self.output_dir = AIStorage.get_instance(
            ).get_user_config().get_value("text2img_output_dir")
        
        if os.getenv("TEXT2IMG_DEFAULT_MODEL") is not None:
            self.default_model = os.getenv("TEXT2IMG_DEFAULT_MODEL")
        else:
            self.default_model = AIStorage.get_instance(
            ).get_user_config().get_value("text2img_default_model")

        if self.url is None:
            logger.error("local stability url is None!")
            return False

        if self.default_model is None:
            logger.error("local stability default model is None!")
            return False

        if self.output_dir is None:
            self.output_dir = "./"
        
        self.output_dir = os.path.abspath(self.output_dir)

        self.start()

        return True

    async def push_task(self, task: ComputeTask, proiority: int = 0):
        logger.info(f"stability_node push task: {task.display()}")
        self.task_queue.put_nowait(task)

    async def remove_task(self, task_id: str):
        pass

    def _make_post_request(self, url, json) -> Tuple[str, requests.Response]:
        try:
            response = requests.post(url, json=json)
            if response.status_code != 200:
                return f'{response.status_code}, {response.json()}', None
            return None, response
        except Exception as e:
            return f"{e}", None


    def _run_task(self, task: ComputeTask):
        task.state = ComputeTaskState.RUNNING
        result = ComputeTaskResult()
        result.result_code = ComputeTaskResultCode.ERROR
        result.set_from_task(task)
        
        model_name = task.params["model_name"]
        prompt = task.params["prompt"]
        negative_prompt = task.params["negative_prompt"]
        if negative_prompt == None or negative_prompt == "":
            negative_prompt = "sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, duplicate, mutated hands, mutated legs, (blurry:1.3), (bad anatomy:1.2), bad proportions, extra limbs, more than 2 nipples, extra legs, fused fingers, missing fingers, jpeg artifacts, signature, watermark, username, artist name, heterochromia, muscular legs, monochrome, grayscale, skin spots, acnes, skin blemishes, age spot, skin spots, acnes, logo, badhandv4, easynegative, cropped image, patreon,lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, ng_deepnegative_v1_75t, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry,(Tiptoe:1.3),looking at viewer, Twisted eyes"

        prompt += ",masterpiece, best quality:1.3"

        logging.info(f"call local stability {model_name} prompts: {prompt}, nagative_prompt: {negative_prompt}")

        if model_name is not None:
            payload = {
                "sd_model_checkpoint": model_name,
            }
            err, resp = self._make_post_request(f'{self.url}/sdapi/v1/options', payload)

            if err is not None:
                task.state = ComputeTaskState.ERROR
                err_msg = f"Set local stability model failed. err:{err}"
                logger.error(err_msg)
                task.error_str = err_msg
                result.error_str = err_msg
                return result

            logging.info(f"set local stability model {model_name} success")

        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": 20
        }

        err, resp = self._make_post_request(f'{self.url}/sdapi/v1/txt2img', payload)
        if err is not None:
            task.state = ComputeTaskState.ERROR
            err_msg = f"Failed. err:{err}"
            logger.error(err_msg)
            task.error_str = err_msg
            result.error_str = err_msg
            return result
        
        r = resp.json()

        for i in r['images']:
            image = Image.open(io.BytesIO(
                base64.b64decode(i.split(",", 1)[0])))
            file_name = os.path.join(self.output_dir, task.task_id + ".png")
            image.save(file_name)

            task.state = ComputeTaskState.DONE
            result.result_code = ComputeTaskResultCode.OK
            result.worker_id = self.node_id
            result.result = {"file": file_name}

            return result

        task.error_str = "Unknown error!"
        result.error_str = "Unknown error!"
        task.state = ComputeTaskState.ERROR
        return result

    def start(self):
        if self.is_start:
            return
        self.is_start = True

        async def _run_task_loop():
            while True:
                logger.info("local_stability_node is waiting for task...")
                task = await self.task_queue.get()
                logger.info(f"stability_node get task: {task.display()}")
                result = self._run_task(task)
                # if result is not None:
                #     task.state = ComputeTaskState.DONE
                #     task.result = result

        asyncio.create_task(_run_task_loop())

    def display(self) -> str:
        return f"Stability_ComputeNode: {self.node_id}"

    def get_task_state(self, task_id: str):
        pass

    def get_capacity(self):
        pass

    def is_support(self, task: ComputeTask) -> bool:
        return task.task_type == ComputeTaskType.TEXT_2_IMAGE

    def is_local(self) -> bool:
        return False
