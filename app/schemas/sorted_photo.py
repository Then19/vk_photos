from enum import Enum

from app.databases.clickhouse.modeles.vk_photo import VkPhotoORM


class SortedPhoto(str, Enum):
    NEW_UPLOAD = "NEW_UPLOAD"
    OLD_UPLOAD = "OLD_UPLOAD"

    NEW_PHOTO = "NEW_PHOTO"
    OLD_PHOTO = "OLD_PHOTO"

    def get_sorted_key(self):
        if self.value == self.NEW_UPLOAD:
            return VkPhotoORM.updated_at.desc()
        if self.value == self.OLD_UPLOAD:
            return VkPhotoORM.updated_at.asc()
        if self.value == self.NEW_PHOTO:
            return VkPhotoORM.image_date.desc()
        if self.value == self.OLD_PHOTO:
            return VkPhotoORM.image_date.asc()