# pylint:disable=E0402
import logging

from ..proto.compute_task import LLMPrompt

class AIRole:
    def __init__(self) -> None:
        self.agent_instance_id : str = None
        self.role_name : str = None
        self.role_id :str = None # $workflow_id.$sub_workflow_id.$role_name
        self.fullname : str = None
        self.agent_name : str = None
        self.prompt : LLMPrompt = None
        self.introduce : str = None
        self.agent = None
        self.enable_function_list : list[str] = None
        self.history_len = 10

    def load_from_config(self,config:dict) -> bool:
        name_node = config.get("name")
        if name_node is None:
            logging.error("role name is not found!")
            return False
        self.role_name = name_node


        agent_id_node = config.get("agent")
        if agent_id_node is None:
            logging.error("agent id is not found!")
            return False
        self.agent_name = agent_id_node

        prompt_node = config.get("prompt")
        if prompt_node:
            self.prompt = LLMPrompt()
            if self.prompt.load_from_config(prompt_node) is False:
                logging.error("load prompt failed!")
                return False

        intro_node = config.get("intro")
        if intro_node is not None:
            self.introduce = intro_node

        history_node = config.get("history_len")
        if history_node is not None:
            self.history_len = int(history_node)

        if config.get("enable_function") is not None:
            self.enable_function_list = config["enable_function"]

    def get_role_id(self) -> str:
        return self.role_id

    def get_intro(self) -> str:
        return self.introduce

    def get_name(self) -> str:
        return self.role_name

    def get_prompt(self) -> LLMPrompt:
        return self.prompt

class AIRoleGroup:
    def __init__(self) -> None:
        self.roles : dict[str,AIRole] = {}
        self.owner_name : str = None

    def load_from_config(self,config:dict) -> bool:
        for k,v in config.items():
            role = AIRole()
            if role.load_from_config(v) is False:
                logging.error(f"load role {k} failed!")
                return False
            role.role_id = self.owner_name + "." + k
            self.roles[k] = role

        return True

    def get(self,role_name:str) -> AIRole:
        return self.roles.get(role_name)

