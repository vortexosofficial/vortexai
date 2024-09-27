from abc import ABC, abstractmethod
import logging
from typing import Coroutine

from ..proto.agent_msg import AgentMsg
from .bus import AIBus

logger = logging.getLogger(__name__)

class AgentTunnel(ABC):
    _all_loader = {}
    _all_tunnels = {}
    @classmethod
    def register_loader(cls,tunnel_type:str,loader:Coroutine) -> None:
        cls._all_loader[tunnel_type] = loader


    @classmethod
    async def load_all_tunnels_from_config(cls,config:dict) -> None:
        for tunnel_id,tunnel_config in config.items():
            loader = cls._all_loader.get(tunnel_config["type"])
            tid = tunnel_config.get("tunnel_id")
            if tid is not None:
                if tunnel_id != tid:
                    logger.warning(f"load tunnel {tunnel_id} error,{tunnel_id} != {tid} in config!")
                    continue
            else:
                tunnel_config["tunnel_id"] = tunnel_id

            if loader is not None:
                tunnel = await loader(tunnel_config)
                if tunnel is not None:
                    cls._all_tunnels[tunnel_id] = tunnel
                    tunnel.connect_to(AIBus.get_default_bus(),tunnel.target_id)
                    await tunnel.start()
                else:
                    logger.error(f"load tunnel {tunnel_id} failed")
            else:
                logger.error(f"load tunnel {tunnel_id} failed,loader not found")

    @classmethod
    async def load_tunnel_from_config(cls,tunnel_config:dict):
        loader = cls._all_loader.get(tunnel_config["type"])
        if loader is not None:
            tunnel = await loader(tunnel_config)
            if tunnel is not None:
                cls._all_tunnels[tunnel.tunnel_id] = tunnel
                tunnel.connect_to(AIBus.get_default_bus(),tunnel.target_id)
                await tunnel.start()
                return True
            else:
                logger.error(f"load tunnel {tunnel_config['tunnel_id']} failed")
        else:
            logger.error(f"load tunnel {tunnel_config['type']} failed,loader not found")

        return False

    @classmethod
    async def get_tunnel_by_agentid(cls,agent_id:str):
        result = []
        for tunnel in cls._all_tunnels.values():
            if tunnel.target_id == agent_id:
                result.append(tunnel)
        return result


    def __init__(self) -> None:
        super().__init__()
        self.tunnel_id = None
        self.target_id = None
        self.target_type = None
        self.ai_bus: AIBus = None
        self.is_connected = False

    def connect_to(self, ai_bus:AIBus,target_id: str) -> None:
        """
        Connect to the agent with the given id
        """
        if self.is_connected:
            logger.warning(f"tunnel {self.tunnel_id} is already connected to {self.target_id}")
            return
        self.target_id = target_id
        self.target_type = "agent"
        self.ai_bus = ai_bus
        self.is_connected = True

    @abstractmethod
    def post_message(self, msg: AgentMsg) -> None:
        pass


    @abstractmethod
    async def start(self) -> bool:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def _process_message(self, msg: AgentMsg) -> None:
        pass
