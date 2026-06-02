from typing import List

from ..config.manager import manager
from ..number import remove_escape_string1


def remove_escape_string(filename: str, replace_char: str = "") -> str:
    """
    移除文件名中的特殊字符
    
    Args:
        filename: 原始文件名
        replace_char: 替换字符，默认为空
    
    Returns:
        处理后的文件名
    """
    return remove_escape_string1(filename, manager.computed.escape_string_list, replace_char)


def deal_actor_more(actor: str) -> str:
    """
    处理演员列表，当超过最大显示数量时添加省略标记
    
    Args:
        actor: 演员列表字符串，用逗号分隔
    
    Returns:
        处理后的演员列表
    """
    actor_name_max: int = int(manager.config.actor_name_max)
    actor_name_more: str = manager.config.actor_name_more
    actor_list: List[str] = actor.split(",")
    
    if len(actor_list) > actor_name_max:  # 演员多于设置值时
        result: str = ""
        for i in range(actor_name_max):
            result += actor_list[i] + ","
        return result.strip(",") + actor_name_more
    
    return actor
