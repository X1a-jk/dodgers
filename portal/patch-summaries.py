from bs4 import BeautifulSoup
import re, os

base = r'D:\baseball\report'
index_path = os.path.join(base, 'index.html')
html = open(index_path, encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

new_summaries = {
    'Edwin Díaz': 'Edwin Díaz 是当今 MLB 最具压制力的终结者之一，职业生涯多次入选全明星，2022 年曾创下单季 1.31 ERA、118 次三振、32 次救援成功的历史级成绩。他以 elite 级别的四缝线速球和锐利滑球组合闻名，2025 年在大都会仍缴出 1.63 ERA、0.87 WHIP 的顶级表现。2026 年因伤病长期缺阵，回归后小样本表现挣扎，但凭过往履历与完整武器库，仍是道奇季后赛牛棚最具威慑力的终结者候选。',
    'Jonathan Hernández': 'Jonathan Hernández 是一名具备不错速球-滑球基础的右投后援，2026 年在道奇牛棚中主要担任深度后援/长中继角色，负责在球队大幅领先或落后时消耗局数，保护核心后援手臂。他的三振能力中等，但 BB/9 接近 4.6，控球与被长打控制仍是瓶颈。30 岁的他若无明显进步，长期前景将停留在名单边缘。',
    'Enrique Hernández': "Enrique 'Kiké' Hernández 是道奇阵中最具代表性的多功能工具人，能在二垒、游击、三垒与外野多个位置提供联盟平均以上的防守，打击以全垒打和面对左投见长。2026 年上半季因伤长期缺阵，8 月才回归，目前处于找回节奏阶段。34 岁的他运动能力虽有所下滑，但防守弹性与更衣室价值仍是道奇不可或缺的部分。",
    'Seth Halvorsen': "Seth Halvorsen 是道奇农场体系中的年轻右投，2024 年完成大联盟首秀，速球具备不错潜力，但变化球和控球仍在发展中。2026 年大联盟样本极小，目前更属于 40 人名单末端的深度后援/未来牛棚潜力股。他的身体条件（6'2\" / 243 lbs）具备耐用型牛棚投手的体型，若能提升控球和变化球品质，有望在未来 1-2 年站稳脚跟。",
    'Alex Call': 'Alex Call 是一名以选球和防守见长的右打外野手，2026 年在道奇担任外野深度替补。本季 AVG .246、OPS .669、HR 1，攻击火力不算突出，但能提供稳定的外野防守与板凳深度。他在小联盟有不错的上垒履历，大联盟定位偏向第四/第五外野与代跑、代守工具人。',
    'Teoscar Hernández': 'Teoscar Hernández 是一名以力量见长的右打外野手，2026 年加入道奇后担任左外野主力，具备稳定中段打线与 25+ 轰级别的长打产能。他的臂力是外野守备亮点，能胜任外野三个位置。2026 年截至目前 OPS .714，与生涯平均接近，但相较 2024 年道奇赛季的 .840 OPS 有明显下滑，需在赛季末提升长打效率。',
    'Ryan Ward': 'Ryan Ward 是道奇自家农场出身的左打外野手，2026 年目前位于小联盟持续发展中。本季大联盟小样本 AVG .218、OPS .738、HR 3，展现一定长打潜力但打击稳定性不足。他的主要价值在于外野防守与左打炮仗，是道奇外野深度与未来替补的潜在选择。',
    'Dalton Rushing': 'Dalton Rushing 是道奇队备受期待的年轻左打捕手，2026 年因手肘炎症位于 10 天伤病名单。本季大联盟小样本 AVG .257、OPS .820、HR 12，已展现出不俗的进攻潜力与长打能力。他的接捕与配球仍在成长中，但进攻型捕手的天赋能让他未来与 Will Smith 形成重要互补。',
    'Alex Freeland': 'Alex Freeland 是道奇自家农场出身的右打内野手，2026 年主要在小联盟发展。本季大联盟小样本 AVG .231、OPS .622、HR 3，守备弹性覆盖二垒、游击、三垒。他的优势在于防守多位置与机动性，打击仍处于适应大联盟阶段，是道奇内野深度的未来储备。',
    'Eliezer Alfonzo': 'Eliezer Alfonzo 是道奇队中的替补捕手，2026 年因 Will Smith 与 Dalton Rushing 伤病曾获得短暂机会。本季大联盟小样本 AVG .188、OPS .501，攻击贡献有限，主要价值在于接捕防守与担任后援捕手。他属于 40 人名单末端的深度选择，常在主力捕手缺阵时作为救火队员。',
    'Hyeseong Kim': 'Hyeseong Kim（金慧成）是道奇从韩职棒签来的内野好手，2026 年目前在小联盟适应北美环境。本季大联盟小样本 AVG .259、OPS .651、HR 1，以接触能力、速度与内野守备见长。他有望成为道奇未来的内野工具人与二垒选择，特别是在排兵布阵上提供额外的右打选项。',
    'Evan Phillips': 'Evan Phillips 是道奇 2024 年世界大赛冠军队的重要后援成员，以刁钻的滑球与变速球组合著称，2024 年曾缴出 2.43 ERA、0.88 WHIP 的 elite 成绩。2026 年他因伤缺席大部分赛季，仅 6.2 局 ERA 6.75、WHIP 1.35 的极小样本不足以评判。健康时的 Phillips 仍是道奇牛棚值得信赖的 setup man 与终结者候选。',
    'Max Muncy': 'Max Muncy 是道奇队近年来最具代表性的力量型左打者之一，以高保送率、强劲拉打力量和大赛经验闻名。2026 年 35 岁的他仍维持 .259/.354/.488、.842 OPS 的高效产出，长打率 .488 显示他的 power tool 并未衰退，是道奇打线中重要的 middle-of-the-order bat 与三垒/一垒守备选择。',
    'Kyle Tucker': 'Kyle Tucker 是当今大联盟最具天赋的右外野手之一，以卓越的力量-速度组合、顶级选球能力和金手套级别的防守著称。他在 2025 年于小熊队打出 .266/.377/.464、22 轰、25 盗的精英赛季，2026 年加盟道奇后虽然长打数据有所下滑，但 .341 的上垒率仍显示其出色的 plate discipline。',
    'Mookie Betts': 'Mookie Betts 是当今 MLB 最全面的球员之一，2018 年美联 MVP 得主，以精英级别的打击能力、出色的速度和顶级的防守闻名。2024 年加盟道奇后转型游击手并帮助球队夺冠，2026 年持续提供稳定的上垒与跑垒价值，并能在游击、二垒、外野多位置切换，是道奇攻防两端的核心引擎。'
}

updated = 0
for art in soup.find_all('article', class_='player-card'):
    h3 = art.find('h3')
    if not h3:
        continue
    name = h3.get_text(strip=True)
    if name not in new_summaries:
        continue
    stat_line = art.find('p', class_='stat-line')
    if stat_line:
        stat_line.string = new_summaries[name]
        updated += 1

open(index_path, 'w', encoding='utf-8').write(str(soup))
print(f'updated {updated} players in {index_path}')
