# TMDB Scraper <a name="tmdb-scraper-zh"></a>
<a href="#tmdb-scraper-en">Switch to English</a>

使用 TMDB Scraper（下文简称 TMDBS）可以从 [TMDB](https://www.themoviedb.org/) 上抓取电视节目的剧集数据。它可以通过 TMDB API 获取指定电视节目的剧集信息，包括剧集的季数、集编号、播出日期、时长、名字和分集剧情等等，还可以选择下载对应的剧集图片。

## 示例
假如你要获取《[黑镜](https://www.themoviedb.org/tv/42009-black-mirror)》[第一季](https://www.themoviedb.org/tv/42009-black-mirror/season/1)的剧集信息，使用 TMDBS 后，你会得到一个包含以下内容的名为 `黑镜 - S01.txt` 的文件：
```
1;2011/12/4;45;国歌;备受爱戴的苏珊娜公主遭人绑架，这让首相麦克尔·凯罗陷入了可怕的两难境地。
2;2011/12/11;62;一千五百万点;一位女士未能在歌唱比赛中受到评委的青睐，她必须做出选择，进行有辱人格的表演还是回到奴隶般的生活状态。
3;2011/12/18;50;你的人生;在不久的将来，每个人都可以使用一种记忆植入装置，了解人类做过、看过和听过的所有事情。
```
每行代表一集的信息，内容为 `集编号;播出日期;时长;名字;分集剧情`。

假如你还设置了下载剧集图片，那么你还会得到一个名为 `黑镜 - S01` 的文件夹，里面有 `1.jpg`、`2.jpg` 和 `3.jpg` 三张图片，分别为第一集、第二集和第三集的默认剧照（若存在）。

## 运行条件
- 安装了 Python 3.9 或更高版本。
- 使用命令 `pip3 install -r requirements.txt` 安装了必要的第三方库。
- 有可用的 TMDB API。（可在 TMDB 账号设置中免费申请）

## 配置说明
在使用 TMDBS 前，请先参考以下提示（示例）对 `config.ini` 进行配置。
```
[TMDB]
# 你的 TMDB API 密钥，请在你的 TMDB 账号设置中查看 API 密钥
API_KEY = YOUR_TMDB_API_KEY
# 你要获取的电视节目的 TMDB ID，电视节目的 TMDB 条目网址末尾的纯数字部分就是 ID
TV_ID = 42009
# 你要获取的电视节目的季数，多季用英文逗号隔开
SEASONS = 1,2,3

[OPTIONS]
# 是否下载剧集图片（剧照），TRUE 为下载，FALSE 为不下载
DOWNLOAD_BACKDROPS = TRUE
# 你要获取的数据的语言，如 zh-CN 表示汉语，en-US 表示英语，以 TMDB 使用的语言代码为准
LANGUAGE = zh-CN
```

## 使用方法
1. 通过 [Releases](https://github.com/x1ao4/tmdb-scraper/releases) 下载最新版本的压缩包并解压到本地目录中。
2. 用记事本或文本编辑打开目录中的 `config.ini` 文件，填写你的 TMDB API 密钥（`API_KEY`）和你要获取的电视节目的相关信息，按照需要设置其他配置选项。
3. 双击 `tmdb-scraper.bat`（Windows）或 `tmdb-scraper.command`（Mac）即可启动 TMDBS。
4. TMDBS 将根据配置信息自动获取指定电视节目的指定季的剧集信息和图片（若存在），并在控制台显示处理结果。剧集信息将保存在脚本所在文件夹内的名为 `电视节目名称 - 季数.txt` 的文件内，剧集图片将保存在脚本所在文件夹内的名为 `电视节目名称 - 季数` 的文件夹内，以集编号命名（若设置了下载剧集图片）。

## 注意事项
- 使用脚本时，请确保你的网络连接正常，并且 TMDB 网站可以正常访问。
- 请确保你提供了有效的 TMDB API 密钥，否则将无法获取数据。
- 若剧集信息发生了变更，重新运行脚本将使用新的剧集信息覆盖旧的剧集信息。

## 赞赏
如果你觉得这个项目对你有用，可以考虑请我喝杯咖啡或者给我一个⭐️。谢谢你的支持！

<img width="399" alt="赞赏" src="https://github.com/user-attachments/assets/bdd2226b-6282-439d-be92-5311b6e9d29c">
<br><br>
<a href="#tmdb-scraper-zh">回到顶部</a>
<br>
<br>
<br>

# TMDB Scraper <a name="tmdb-scraper-en"></a>
<a href="#tmdb-scraper-zh">切换至中文</a>

TMDB Scraper (hereafter referred to as TMDBS) allows you to fetch episode data for TV shows from [TMDB](https://www.themoviedb.org/) via the TMDB API. It retrieves information such as Season Numbers, Episode Numbers, Air Dates, Runtimes, Names, and Episode Overviews, and optionally downloads the corresponding Episode Backdrops.

## Example
Suppose you want to fetch episode data for [Season 1](https://www.themoviedb.org/tv/42009-black-mirror/season/1) of '[Black Mirror](https://www.themoviedb.org/tv/42009-black-mirror)'. After using TMDBS, you will get a file named `Black Mirror - S01.txt` containing the following content:
```
1;12/4/2011;45;The National Anthem;Prime Minister Michael Callow faces a shocking dilemma when Princess Susannah, a much-loved member of the Royal Family, is kidnapped.
2;12/11/2011;62;Fifteen Million Merits;In a world where people’s lives consist of riding exercise bikes to gain credits, Bing tries to help a woman get on to a singing competition show.
3;12/18/2011;50;The Entire History of You;In the near future, everyone has access to a memory implant that records everything humans do, see and hear.
```
Each line represents one episode with the format: `Episode Number;Air Date;Runtime;Name;Episode Overview`.

If you've enabled episode backdrop download, you'll also get a folder named `Black Mirror - S01` containing images named `1.jpg`, `2.jpg`, and `3.jpg`, which are the default stills for episodes 1, 2, and 3 (if available).

## Requirements
- Python 3.0 or higher installed.
- All required dependencies installed using `pip3 install -r requirements.txt`.
- A valid TMDB API key. (available for free in your TMDB account settings)

## Configuration
Before using TMDBS, please configure the `config.ini` file according to the following tips (example).
```
[TMDB]
# Your TMDB API key. You can find it in your TMDB account settings.
API_KEY = YOUR_TMDB_API_KEY
# TMDB ID of the target TV show. Numeric ID at the end of the show's TMDB URL.
TV_ID = 42009
# Target seasons. Use commas to separate multiple seasons.
SEASONS = 1,2,3

[OPTIONS]
# Whether to download episode backdrops. TRUE = download, FALSE = don't download.
DOWNLOAD_BACKDROPS = TRUE
# The language code for the data, e.g., zh-CN for Chinese, en-US for English. Follow TMDB language codes.
LANGUAGE = zh-CN
```

## How to Use
1. Download the latest release package from [Releases](https://github.com/x1ao4/tmdb-scraper/releases) and extract it to a local directory.
2. Open the `config.ini` file in the directory with a text editor, fill in your TMDB API key (`API_KEY`) and the relevant TV show info. Adjust other settings as needed.
3. Double-click `tmdb-scraper.bat` (Windows) or `tmdb-scraper.command` (Mac) to start TMDBS.
4. TMDBS will automatically retrieve the episode information and backdrops (if available) for the specified seasons of the specified show based on your configuration, and display the result in the console. The episode information will be saved in a file named `TV Show Title - Season Number.txt` in the folder where the script is located, and the episode backdrops will be saved in a folder named `TV Show Title - Season Number` in the folder where the script is located, named after the episode number (if backdrop download is enabled).

## Notes
- Make sure you have a stable internet connection and that the TMDB website is accessible.
- A valid TMDB API key is required; otherwise, the script won't be able to fetch data.
- If episode data changes, rerunning the script will overwrite the old data with the latest.

## Support
If you found this helpful, consider buying me a coffee or giving it a ⭐️. Thanks for your support!

<img width="399" alt="Support" src="https://github.com/user-attachments/assets/bdd2226b-6282-439d-be92-5311b6e9d29c">
<br><br>
<a href="#tmdb-scraper-zh">Back to Top</a>
