# 项目名称
BOT_NAME = 'jobsSpider'
SPIDER_MODULES = ['jobsSpider.spiders']
NEWSPIDER_MODULE = 'jobsSpider.spiders'
# 调包引入伪装头库
from jobsSpider.Util.USER_AGENT_LIST import Get_USER_AGENT
# 随机获取一个伪装头
USER_AGENT = Get_USER_AGENT()
# 编码格式
FEED_EXPORT_ENCODING='UTF-8'
# 遵守机器人协议
ROBOTSTXT_OBEY = False
# 管道类引入
ITEM_PIPELINES = {
   'jobsSpider.pipelines.JobsMySQLPipeline': 200,
   'jobsSpider.pipelines.JobsFilePipeline':600,
}
# 设置日志输出的种类（ERROR：一般错误，WARNING：警告，INFO：一般的信息，DEBUG：调试信息）
LOG_LEVEL = "DEBUG"
# 设置日志输入的目录
# LOG_FILE = 'log.txt'
# 设置采集时间间隔
DOWNLOAD_DELAY = 2
# 启动间隔协议
RANDOMIZE_DOWNLOAD_DELAY = True