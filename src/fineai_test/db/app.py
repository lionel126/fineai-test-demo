from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, JSON, PrimaryKeyConstraint, Sequence, String, Text, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Job(Base):
    __tablename__ = 'job'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='job_pkey'),
        {'comment': '任务表'}
    )

    id = mapped_column(String(50), comment='主键')
    user_model_id = mapped_column(BigInteger, nullable=False, comment='用户分身ID')
    job_kind = mapped_column(String(20), nullable=False, comment='任务类型:output-出图,hd-高清图')
    priority = mapped_column(Integer, nullable=False, server_default=text('5'))
    is_delete = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否删除')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    params = mapped_column(JSON, comment='任务所需参数模板/基模/等')
    status = mapped_column(String(10), server_default=text("'create'::character varying"), comment='任务状态:pending-初始化,running-运行中,success-成功,fail-失败,delete-删除')
    theme_param = mapped_column(JSON, comment='主题/模板相关参数')
    result = mapped_column(JSON, comment='响应结果')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='orders_pkey'),
        {'comment': '订单交易表'}
    )

    id = mapped_column(BigInteger, Sequence('orders_seq'), comment='主键')
    order_no = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='订单号')
    transaction_no = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='三方交易号')
    platform = mapped_column(String(50), nullable=False, comment='小程序平台')
    user_id = mapped_column(BigInteger, nullable=False, comment='支付用户ID')
    app_id = mapped_column(String(50), nullable=False, comment='小程序appId')
    openid = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='用户openid')
    amount = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='支付金额单位分')
    amount_refunded = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='订单退款金额单位分')
    order_type = mapped_column(String(30), nullable=False, server_default=text("'charge'::character varying"), comment='订单类型:charge-消费,refund-退款')
    status = mapped_column(String(10), nullable=False, server_default=text("'init'::character varying"), comment='订单状态:init-初始化,success-成功,fail-失败,timeout-超时,refund-退款')
    user_ip = mapped_column(String(30), nullable=False, server_default=text("''::character varying"), comment='用户下单IP')
    source_id = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='原订单或者父级订单ID')
    product_id = mapped_column(String(30), nullable=False, server_default=text("''::character varying"), comment='商品ID')
    product_type = mapped_column(String(30), nullable=False, server_default=text("''::character varying"), comment='商品类型:recharge-充值,model-用户分身商品')
    channel = mapped_column(String(20), nullable=False, server_default=text("'JSAPI'::character varying"), comment='支付渠道:JSAPI')
    merchant_no = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='支付商户号')
    expired_time = mapped_column(DateTime, nullable=False, comment='订单到期时间')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='订单更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='订单创建时间')
    user_agent = mapped_column(Text, comment='用户下单UA')
    trade_time = mapped_column(DateTime, comment='交易发生时间')


class OutputImageFile(Base):
    __tablename__ = 'output_image_file'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='output_image_file_pkey'),
        {'comment': '用户分身图文件表'}
    )

    id = mapped_column(BigInteger, Sequence('output_image_file_seq'), comment='主键')
    job_id = mapped_column(String(50), nullable=False, comment='任务Id')
    image_type = mapped_column(String(50), nullable=False, server_default=text("'model'::character varying"), comment='用户分身生成图类型:avatar-头像,model-分身')
    path = mapped_column(String(200), nullable=False, server_default=text("''::character varying"), comment='文件路径：/{bucketName}/{key}')
    hd_id = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='高清图片ID,每个图片仅生成一张高清')
    status = mapped_column(String(10), nullable=False, server_default=text("'create'::character varying"), comment='文件状态:pending-生成中,finish-完成,fail-失败,delete-删除')
    is_delete = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否删除')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class ProductRecharge(Base):
    __tablename__ = 'product_recharge'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='product_recharge_pkey'),
        {'comment': '充值商品表'}
    )

    id = mapped_column(BigInteger, Sequence('product_recharge_seq'), comment='主键')
    product_id = mapped_column(String(50), nullable=False, comment='商品Id')
    title = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='商品名称')
    coin = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='金币数量')
    free_coin = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='赠送金币')
    price = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='商品标价')
    order_by = mapped_column(Integer, nullable=False, server_default=text('0'), comment='商品顺序')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    brief = mapped_column(Text, comment='商品摘要')
    style = mapped_column(String(100), comment='商品样式配置')
    status = mapped_column(String(10), server_default=text("'on_sale'::character varying"), comment='商品状态:on_sale,off_sale')


class SystemBaseModel(Base):
    __tablename__ = 'system_base_model'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='system_base_model_pkey'),
        {'comment': '系统基础模型模板参数表'}
    )

    id = mapped_column(BigInteger, Sequence('system_base_model_seq'), comment='主键')
    title = mapped_column(String(100), nullable=False, server_default=text("''::character varying"), comment='标题')
    used = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否使用')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    default_param = mapped_column(JSON, comment='参数默认值')
    config = mapped_column(JSON, comment='配置模板')


class SystemConfig(Base):
    __tablename__ = 'system_config'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='system_config_pkey'),
        {'comment': '系统配置表'}
    )

    id = mapped_column(BigInteger, Sequence('system_config_seq'), comment='系统参数值')
    config_key = mapped_column(String(30), nullable=False, comment='系统参数key')
    config_value = mapped_column(Text)
    description = mapped_column(Text)


class SystemTheme(Base):
    __tablename__ = 'system_theme'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='system_theme_pkey'),
        {'comment': '系统主题表'}
    )

    id = mapped_column(BigInteger, Sequence('system_theme_seq'), comment='主键')
    title = mapped_column(String(100), nullable=False, server_default=text("''::character varying"), comment='标题')
    poster = mapped_column(String(100), nullable=False, server_default=text("''::character varying"), comment='海报图')
    status = mapped_column(String(10), nullable=False, server_default=text("'on_sale'::character varying"), comment='主题状态:on_sale-上架,off_sale-下架')
    order_by = mapped_column(Integer, nullable=False, server_default=text('0'), comment='排序数字越大顺序越靠前')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    style = mapped_column(JSON, comment='风格')
    model = mapped_column(JSON, comment='造型数据')
    default_param = mapped_column(JSON, comment='参数')
    config = mapped_column(JSON, comment='配置参数')


class UploadImageFile(Base):
    __tablename__ = 'upload_image_file'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='upload_image_file_pkey'),
        {'comment': '用户分身图文件表'}
    )

    id = mapped_column(BigInteger, Sequence('upload_image_file_seq'), comment='主键')
    user_model_id = mapped_column(BigInteger, nullable=False, comment='用户分身ID')
    image_type = mapped_column(String(50), nullable=False, server_default=text("'model'::character varying"), comment='图片上传用户:personal-个人;model-训练模型;')
    path = mapped_column(String(200), nullable=False, server_default=text("''::character varying"), comment='文件路径：/{bucketName}/{key}')
    reason = mapped_column(String(100), nullable=False, server_default=text("''::character varying"), comment='失败原因')
    status = mapped_column(String(10), nullable=False, server_default=text("'create'::character varying"), comment='文件状态:uploading-上传中,finish-完成,fail-失败,delete-删除')
    is_delete = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否删除')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    job_id = mapped_column(String(50), comment='任务Id')


class UserAccount(Base):
    __tablename__ = 'user_account'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_account_pkey'),
        {'comment': '用户账户表'}
    )

    id = mapped_column(BigInteger, Sequence('user_account_seq'), comment='主键')
    user_id = mapped_column(BigInteger, nullable=False)
    account_type = mapped_column(String(32), nullable=False, comment='账户类型:balance')
    balance = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"), comment='账户余额')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class UserAccountLog(Base):
    __tablename__ = 'user_account_log'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_account_log_pkey'),
        {'comment': '用户账户日志表'}
    )

    id = mapped_column(BigInteger, Sequence('user_account_log_seq'), comment='主键')
    account_id = mapped_column(BigInteger, nullable=False, comment='账户ID')
    op_type = mapped_column(String(32), nullable=False, comment='账户操作类型:recharge-充值,refund-退款,charge-消费')
    balance_before = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"), comment='账户变动前余额')
    op_balance = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"), comment='账户变动余额')
    balance_after = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"), comment='账户变动后余额')
    ref_id = mapped_column(String(64), nullable=False, comment='账户变动关联的唯一标识,例如订单号')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    remark = mapped_column(String(128), comment='备注')


class UserBase(Base):
    __tablename__ = 'user_base'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_base_pkey'),
        {'comment': '用户基础信息表'}
    )

    id = mapped_column(BigInteger, Sequence('user_base_seq'), comment='主键')
    phone_number = mapped_column(String(30), nullable=False, server_default=text("''::character varying"), comment='用户手机号,国外带区号')
    pure_phone_number = mapped_column(String(20), nullable=False, server_default=text("''::character varying"), comment='没有区号的手机号')
    country_code = mapped_column(String(10), nullable=False, server_default=text("''::character varying"), comment='区号')
    status = mapped_column(String(10), nullable=False, server_default=text("'enable'::character varying"), comment='用户状态:enable,disable')
    login_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='最近一次登录时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间注册时间')
    user_agent = mapped_column(Text, comment='用户第一次注册UA')


class UserBaseInfo(Base):
    __tablename__ = 'user_base_info'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_base_info_pkey'),
        {'comment': '用户辅助信息表'}
    )

    id = mapped_column(BigInteger, Sequence('user_base_info_seq'), comment='主键')
    user_id = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='用户基础信息表ID')
    platform = mapped_column(String(10), nullable=False, server_default=text("''::character varying"), comment='应用平台:wx,dy')
    app_id = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='平台下appId')
    union_id = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='用户union_id')
    openid = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='用户openid')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    comment = mapped_column(Text, comment='备注信息')


class UserJobImage(Base):
    __tablename__ = 'user_job_image'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_job_image_pkey'),
        {'comment': '用户分身出图列表'}
    )

    id = mapped_column(String(50), comment='主键')
    user_model_id = mapped_column(BigInteger, nullable=False, comment='用户分身ID')
    image_type = mapped_column(String(50), nullable=False, server_default=text("'avatar'::character varying"), comment='图片类型')
    show_name = mapped_column(String(50), nullable=False, server_default=text("'默认'::character varying"), comment='显示名称')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    is_delete = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否删除')
    status = mapped_column(String(10), server_default=text("'create'::character varying"), comment='状态：create-创建,pending-等待,running-处理中,success-成功,fail-失败')


class UserModel(Base):
    __tablename__ = 'user_model'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_model_pkey'),
        {'comment': '用户分身表'}
    )

    id = mapped_column(BigInteger, Sequence('user_model_seq'), comment='主键')
    user_id = mapped_column(BigInteger, nullable=False, comment='用户ID')
    model_name = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='用户分身名')
    gender = mapped_column(Integer, nullable=False, server_default=text('0'), comment='用户性别：0-未知,1-男,2-女')
    image_id = mapped_column(BigInteger, nullable=False, server_default=text('0'), comment='用户头像')
    order_no = mapped_column(String(30), nullable=False, server_default=text("''::character varying"), comment='用户分身付费订单号')
    status = mapped_column(String(10), nullable=False, server_default=text("'init'::character varying"), comment='用户分身状态:init-个人头像,pending-批量上传,ready-照片合格开始训练,finish-完成,fail-失败')
    pay_status = mapped_column(String(10), nullable=False, server_default=text("'unpaid'::character varying"), comment='分身付费状态:unpaid-未付费,paid-已付费,refund-已退款')
    model_file = mapped_column(String(100), nullable=False, server_default=text("''::character varying"), comment='模型文件')
    job_id = mapped_column(String(50), nullable=False, server_default=text("''::character varying"), comment='模型训练任务Id')
    is_delete = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否删除')
    updated_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='更新时间')
    created_time = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    birthday = mapped_column(Integer, nullable=False, server_default=text('0'), comment='生日')
    finished_time = mapped_column(DateTime, comment='分身生成时间')
