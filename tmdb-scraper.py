import os
import locale
import requests
import configparser
from datetime import datetime

# 判断系统语言是否为中文
def is_system_language_chinese():
    lang, _ = locale.getlocale()
    return lang is not None and lang.startswith('zh')

IS_CHINESE = is_system_language_chinese()

# 提示信息模板
def msg(key, **kwargs):
    messages = {
        'processing': {
            'zh': "\n🚀 正在处理《{title}》的第{season}季...\n",
            'en': "\n🚀 Processing Season {season} of \"{title}\"...\n"
        },
        'saved': {
            'zh': "✅ 第{season}季第{ep}集信息已保存",
            'en': "✅ Season {season} Episode {ep} info saved"
        },
        'updated': {
            'zh': "📝 第{season}季第{ep}集信息已更新",
            'en': "📝 Season {season} Episode {ep} info updated"
        },
        'no_update': {
            'zh': "⚡ 第{season}季没有新的更新",
            'en': "⚡ No new updates for Season {season}"
        },
        'image_saved': {
            'zh': "📸 第{season}季第{ep}集图片已保存",
            'en': "📸 Season {season} Episode {ep} backdrop saved"
        },
        'image_failed': {
            'zh': "❌ 下载图片失败：{url} -> {error}",
            'en': "❌ Failed to download backdrop: {url} -> {error}"
        },
        'summary': {
            'zh': "\n🎉 全部处理完成！{saved}{updated}{images}",
            'en': "\n🎉 All done! {saved}{updated}{images}"
        },
        'saved_summary': {
            'zh': "共保存{count}集信息。",
            'en': "{count} episode(s) saved. "
        },
        'updated_summary': {
            'zh': "共更新{count}集信息。",
            'en': "{count} episode(s) updated."
        },
        'image_summary': {
            'zh': "共保存{count}张图片。",
            'en': "{count} backdrop(s) saved."
        },
        'season_not_found': {
            'zh': "❌ 第{season}季不存在",
            'en': "❌ Season {season} does not exist"
        }
    }

    lang = 'zh' if IS_CHINESE else 'en'
    text = messages[key][lang]
    return text.format(**kwargs)

def format_air_date(date_str, language):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        format_mapping = {
            'zh-CN': f"{dt.year}/{dt.month}/{dt.day}",
            'en-US': f"{dt.month}/{dt.day}/{dt.year}",
            'fr-FR': f"{dt.day:02d}/{dt.month:02d}/{dt.year}",
            'ja-JP': f"{dt.year}/{dt.month:02d}/{dt.day}",
            'de-DE': f"{dt.day:02d}.{dt.month:02d}.{dt.year}",
            'zh-SG': f"{dt.day}/{dt.month}/{dt.year}",
            'ko-KR': f"{dt.year}-{dt.month:02d}-{dt.day}"
        }
        return format_mapping.get(language, date_str)
    except:
        return date_str

def load_config():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read('config.ini', encoding='utf-8')
    return {
        'api_key': config['TMDB']['API_KEY'],
        'tv_id': config['TMDB']['TV_ID'],
        'seasons': [int(s.strip()) for s in config['TMDB']['SEASONS'].split(',')],
        'download_backdrops': config['OPTIONS'].getboolean('DOWNLOAD_BACKDROPS'),
        'language': config['OPTIONS'].get('LANGUAGE', 'zh-CN'),
    }

def get_season_data(api_key, tv_id, season_num, language):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season_num}"
    params = {"api_key": api_key, "language": language}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(msg('season_not_found', season=season_num))
            return None
        else:
            raise e

def get_tv_show_name(api_key, tv_id, language):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}"
    params = {"api_key": api_key, "language": language}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('name', '未知剧名' if IS_CHINESE else 'Unknown Title')

def save_episode_info(episodes, season_num, tv_show_name, total_stats, language):
    if episodes is None:
        return
    file_name = f"{tv_show_name} - S{season_num:02d}.txt"
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()
    else:
        existing_lines = []

    updated_episodes = []
    has_update = False

    for ep in episodes:
        line = f"{ep['episode_number']};{format_air_date(ep['air_date'], language)};{ep['runtime']};{ep['name']};{ep['overview']}".replace('\n', '') + '\n'
        new_content = line.strip().split(';')

        found = False
        for i, existing_line in enumerate(existing_lines):
            existing_content = existing_line.strip().split(';')
            if existing_content[0] == new_content[0]:
                found = True
                if existing_content != new_content:
                    existing_lines[i] = line
                    updated_episodes.append(line)
                    print(msg('updated', season=season_num, ep=ep['episode_number']))
                    total_stats['updated'] += 1
                    has_update = True
                else:
                    updated_episodes.append(line)
                break

        if not found:
            updated_episodes.append(line)
            print(msg('saved', season=season_num, ep=ep['episode_number']))
            total_stats['saved'] += 1
            has_update = True

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_episodes)

    if not has_update:
        print(msg('no_update', season=season_num))

def download_episode_images(episodes, season_num, tv_show_name, total_stats):
    if episodes is None:
        return
    base_url = "https://image.tmdb.org/t/p/original"
    image_dir = os.path.join(os.path.dirname(__file__), f'{tv_show_name} - S{season_num:02d}')
    os.makedirs(image_dir, exist_ok=True)

    for ep in episodes:
        if ep.get('still_path'):
            img_url = base_url + ep['still_path']
            img_path = os.path.join(image_dir, f"{ep['episode_number']}.jpg")

            if os.path.exists(img_path):
                continue

            try:
                with open(img_path, 'wb') as f:
                    f.write(requests.get(img_url).content)
                print(msg('image_saved', season=season_num, ep=ep['episode_number']))
                total_stats['images'] += 1
            except Exception as e:
                print(msg('image_failed', url=img_url, error=e))

def main():
    config = load_config()
    tv_show_name = get_tv_show_name(config['api_key'], config['tv_id'], config['language'])

    total_stats = {'saved': 0, 'updated': 0, 'images': 0}

    for season_num in config['seasons']:
        print(msg('processing', title=tv_show_name, season=season_num))

        season_data = get_season_data(config['api_key'], config['tv_id'], season_num, config['language'])

        if season_data is None:
            continue

        episodes = []
        for ep in season_data.get('episodes', []):
            episodes.append({
                'episode_number': ep.get('episode_number'),
                'air_date': ep.get('air_date', ''),
                'runtime': ep.get('runtime', 0),
                'name': ep.get('name', '').strip(),
                'overview': ep.get('overview', '').strip(),
                'still_path': ep.get('still_path')
            })

        save_episode_info(episodes, season_num, tv_show_name, total_stats, config['language'])

        if config['download_backdrops']:
            download_episode_images(episodes, season_num, tv_show_name, total_stats)

    saved_info = msg('saved_summary', count=total_stats['saved']) if total_stats['saved'] > 0 else ""
    updated_info = msg('updated_summary', count=total_stats['updated']) if total_stats['updated'] > 0 else ""
    image_info = msg('image_summary', count=total_stats['images']) if total_stats['images'] > 0 else ""

    summary = msg('summary', saved=saved_info, updated=updated_info, images=image_info)
    print(summary)

if __name__ == '__main__':
    main()
    