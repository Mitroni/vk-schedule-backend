from config import ADMIN_IDS

def is_admin(vk_user_id: int) -> bool:
    return vk_user_id in ADMIN_IDS