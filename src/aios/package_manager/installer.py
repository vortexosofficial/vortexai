# installer download pkg by cid, than install it to target dir
import logging
import asyncio
import aiohttp
import aiofiles
import os
from typing import Tuple

#from ndn_client import ContentId,NDN_Client
from ..net import ContentId,NDN_Client
from .pkg import PackageInfo,PackageMediaInfo
from .env import PackageEnv

logger = logging.getLogger(__name__)

INSTALL_TASK_STATE_DONE = 0
INSTALL_TASK_STATE_CHECK_DEPENDENCY = 1
INSTALL_TASK_STATE_INSTALL_DEPENDENCY = 2
INSTALL_TASK_STATE_DOWNLOADING = 3
INSTALL_TASK_STATE_INSTALLING = 4
INSTALL_TAKS_STATE_ERROR = 5

class PackageInstallTask:
    def __init__(self,owner:PackageEnv) -> None:
        self.owner = owner
        self.state = INSTALL_TASK_STATE_CHECK_DEPENDENCY

        self.pkg_media_info = None
        self.working_task = None
        self.dependency_tasks = None
        self.error_str = None

class PackageInstaller:
    def __init__(self,owner_env:PackageEnv) -> None:
        self.all_tasks = {}
        self.owner_env = owner_env
    
    def install(self,pkg_name:str,
                install_from_dependency = False, can_upgrade = True,skip_depends = False,options = None)->Tuple[PackageInstallTask,str]:

        the_pkg_info : PackageInfo = None
        is_upgrade : bool = False
        need_backup : bool = False
        
        pkg_id,version_str,cid = PackageInfo.parse_pkg_name(pkg_name)
        media_info : PackageMediaInfo = self.owner_env.get_media_info(pkg_name) # must use index-db?
        if media_info is not None:
            if cid is not None:
                if can_upgrade:
                    is_upgrade = True
                else:
                    error_str = f"{pkg_name},{cid} already installed!"
                    logger.error(error_str)
                    return None,error_str
            else:
                the_pkg_info = self.owner_env.lookup(pkg_id,version_str,None)
                if the_pkg_info is None:
                    error_str = f"{pkg_name} old version exist in local but not found in index db!"
                    logger.error(error_str)
                    return None,error_str
                else:
                    is_upgrade = True
                    need_backup = True

        if the_pkg_info is None:
            the_pkg_info = self.owner_env.lookup(pkg_id,version_str,cid)
        
        if the_pkg_info is None:
            error_str = f"{pkg_name} ,cid:{cid} not found in index db"
            logger.error(error_str)
            return None,error_str
        
        result_task = self.all_tasks.get(the_pkg_info.cid)
        if result_task is not None:
            return result_task,"already installing"
        
        logger.info(f"start download&install {pkg_name},install_from_dependency={install_from_dependency},upgrade={is_upgrade},backup={need_backup},target_pkg_info={the_pkg_info}")
        result_task = PackageInstallTask(self.owner_env)
        self.all_tasks[the_pkg_info.cid] = result_task
        async def download_and_install_pkg()->int:
            # check dependency
            if skip_depends is False:
                result_task.dependency_tasks = {}
                self.get_dependency_tasks(the_pkg_info,result_task.dependency_tasks)
                result_task.state = INSTALL_TASK_STATE_INSTALL_DEPENDENCY
                for depend_pkg_name in result_task.dependency_tasks:
                    # check pkg in local?
                    # install miss pkg
                    pass
            
            result_task.state = INSTALL_TASK_STATE_DOWNLOADING
            install_full_path = ""
            target_full_path = ""
            old_package_full_path = ""
            is_download_directy = False

            if the_pkg_info.target_media_type == the_pkg_info.source_media_type:
                is_download_directy = True
                if is_upgrade:
                    target_full_path = ""
                else:
                    target_full_path = ""
            else:
                pass

            urls = self.owner_env.get_pkg_urls(the_pkg_info)
            #download
            client = NDN_Client() # set watch
            download_result = await client.get_file(the_pkg_info.cid,urls,target_full_path,options) 
            if download_result !=0:
                result_task.state = INSTALL_TAKS_STATE_ERROR
                return result_task.state
            
            result_task.state = INSTALL_TASK_STATE_INSTALLING
            if is_download_directy is False:
                install_media_result = False
                install_media_result = await self.owner_env.do_pkg_media_trans(the_pkg_info,target_full_path,install_full_path)
                if install_media_result is False:
                    result_task.state = INSTALL_TAKS_STATE_ERROR
                    result_task.error_str = "install media error,from {target_full_path} to {install_full_path}"
                    return result_task.state
               
            # last step,save install flag : install by manual or install by dependency
            ## save cid dir
            if is_upgrade:
                os.rename(old_package_full_path, old_package_full_path + ".old" )
                os.rename(target_full_path,install_full_path)
            ## update/create version link
            
            ## update pkg state
            ## remove old version
    
            result_task.state = INSTALL_TASK_STATE_DONE
            return result_task.state
                

        result_task.working_task = asyncio.create_task(download_and_install_pkg())
        return result_task,None

        
    def uninstall(self):
        pass
    
    def get_dependency_tasks(self,pkg:PackageInfo,dependency_tasks):
        pass

    async def check_dependency(self,pkg:PackageInfo,task_list:{}) -> bool:
        for depend_pkg_name in pkg.depends:
            depend_task = task_list.get(depend_pkg_name)
            if depend_task is not None:
                logger.debug(f"{pkg.name}'s depend pkg {depend_pkg_name} already in task list")
                continue
            depend_task = PackageInstallTask(self.owner_env)
            task_list[depend_pkg_name] = depend_task
            
            depend_pkg_info = self.owner_env.lookup(depend_pkg_name)
            if depend_pkg_info is None:
                logger.warn(f"{pkg.name}'s depend pkg {depend_pkg_name} not found in index db")
                return False
            
            if await self.check_dependency(depend_pkg_info,task_list) is False:
                return False
    
        return True
        
        

        
        


