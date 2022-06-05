import enum


class UserTypeEnum(str, enum.Enum):
    USER_TYPE_ATTN = 'ATTN'
    USER_TYPE_ADMIN = 'ADMIN'
    USER_TYPE_BUYER = 'BUYER'
    USER_TYPE_SELLER = 'SELLER'
