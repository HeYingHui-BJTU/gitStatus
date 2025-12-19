#!/usr/bin/env python3
"""
禾盈慧 (HeYingHui) Git Repository Statistics Generator
协作洞察工具 - 具有产品思维的团队协作分析系统
"""

import subprocess
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json
import re
import hashlib
from html_template import get_compact_html_template

class GitStatsGenerator:
    # 用户名到真实姓名的映射
    AUTHOR_MAPPING = {
        'Nahjs': '蒲显科',
        'Xianke Pu': '蒲显科',
        'QICY520': '曹棪',
        'YDUTSEVOLDN': '宁苏颜',
        '2301_79648705': '宁苏颜',
        'Jared-1019': '黄光景',
        'Camelli-a': '张琪',
    }
    
    # 为每个作者分配专属颜色（用于可视化）
    AUTHOR_COLORS = {
        '蒲显科': '#667eea',
        '曹棪': '#f59e0b',
        '宁苏颜': '#10b981',
        '黄光景': '#ef4444',
        '张琪': '#8b5cf6',
    }
    
    def __init__(self, repo_path, output_dir, repo_name):
        self.repo_path = os.path.abspath(repo_path)
        self.output_dir = os.path.abspath(output_dir)
        self.repo_name = repo_name
        self.stats = {
            'authors': defaultdict(lambda: {
                'commits': 0,
                'additions': 0,
                'deletions': 0,
                'first_commit': None,
                'last_commit': None,
                'files_changed': set(),
                'commits_by_date': defaultdict(int),
                'commits_by_hour': defaultdict(int),
                'commits_by_weekday': defaultdict(int),
                'merge_commits': 0,
                'impact_score': 0  # 代码当量
            }),
            'by_hour': defaultdict(int),
            'by_weekday': defaultdict(int),
            'by_month': defaultdict(int),
            'by_year': defaultdict(int),
            'by_hour_weekday': defaultdict(lambda: defaultdict(int)),  # 热力图数据
            'file_types': defaultdict(int),
            'total_commits': 0,
            'total_files': 0,
            'total_merge_commits': 0,
            'first_commit_date': None,
            'last_commit_date': None,
            'commit_timeline': [],
            'daily_commits': defaultdict(int)
        }
    
    def normalize_author(self, author):
        """规范化作者名称，使用真实姓名映射"""
        # 尝试精确匹配
        if author in self.AUTHOR_MAPPING:
            return self.AUTHOR_MAPPING[author]
        
        # 尝试部分匹配（不区分大小写）
        author_lower = author.lower()
        for key, value in self.AUTHOR_MAPPING.items():
            if key.lower() in author_lower or author_lower in key.lower():
                return value
        
        # 如果没有匹配，返回原名
        return author
    
    def get_author_color(self, author):
        """获取作者专属颜色"""
        return self.AUTHOR_COLORS.get(author, '#6b7280')
    
    def calculate_impact_score(self, commits, additions, deletions):
        """计算代码当量（Impact Score）
        考虑提交次数和代码变更量的综合影响
        """
        # 简化公式：commits * 10 + additions + deletions * 0.5
        return int(commits * 10 + additions + deletions * 0.5)
    
    def run_git_command(self, cmd):
        """运行 Git 命令并返回输出"""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                shell=False
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error running command {' '.join(cmd)}: {e}")
            return ""
    
    def collect_basic_info(self):
        """收集基本仓库信息"""
        # 总提交数
        output = self.run_git_command(['git', 'rev-list', '--count', 'HEAD'])
        self.stats['total_commits'] = int(output) if output else 0
        
        # 总文件数
        output = self.run_git_command(['git', 'ls-files'])
        files = output.split('\n') if output else []
        self.stats['total_files'] = len([f for f in files if f])
        
        # 文件类型统计
        for f in files:
            if f:
                ext = os.path.splitext(f)[1] or 'no-extension'
                self.stats['file_types'][ext] += 1
    
    def collect_commit_stats(self):
        """收集提交统计信息"""
        # 获取提交日志：时间戳、作者、文件变更统计
        log_format = '%at|%an|%ae|%s'
        output = self.run_git_command([
            'git', 'log', '--all', '--numstat', 
            f'--pretty=format:COMMIT|{log_format}'
        ])
        
        if not output:
            return
        
        lines = output.split('\n')
        current_commit = None
        
        for line in lines:
            if line.startswith('COMMIT|'):
                # 解析提交信息
                parts = line[7:].split('|')
                if len(parts) >= 4:
                    timestamp = int(parts[0])
                    raw_author = parts[1]
                    email = parts[2]
                    subject = parts[3]
                    
                    # 规范化作者名
                    author = self.normalize_author(raw_author)
                    
                    dt = datetime.fromtimestamp(timestamp)
                    date_str = dt.strftime('%Y-%m-%d')
                    
                    # 检测是否为 Merge commit
                    is_merge = bool(re.search(r'\bmerge\b', subject, re.IGNORECASE))
                    
                    current_commit = {
                        'author': author,
                        'timestamp': timestamp,
                        'date': dt,
                        'subject': subject,
                        'additions': 0,
                        'deletions': 0,
                        'files': [],
                        'is_merge': is_merge
                    }
                    
                    # 更新作者统计
                    author_stats = self.stats['authors'][author]
                    author_stats['commits'] += 1
                    author_stats['commits_by_date'][date_str] += 1
                    author_stats['commits_by_hour'][dt.hour] += 1
                    author_stats['commits_by_weekday'][dt.weekday()] += 1
                    
                    if is_merge:
                        author_stats['merge_commits'] += 1
                        self.stats['total_merge_commits'] += 1
                    
                    if author_stats['first_commit'] is None or timestamp < author_stats['first_commit']:
                        author_stats['first_commit'] = timestamp
                    if author_stats['last_commit'] is None or timestamp > author_stats['last_commit']:
                        author_stats['last_commit'] = timestamp
                    
                    # 时间统计
                    self.stats['by_hour'][dt.hour] += 1
                    self.stats['by_weekday'][dt.weekday()] += 1
                    self.stats['by_month'][dt.strftime('%Y-%m')] += 1
                    self.stats['by_year'][dt.year] += 1
                    
                    # 热力图数据：按星期几和小时统计
                    self.stats['by_hour_weekday'][dt.weekday()][dt.hour] += 1
                    
                    # 提交时间线（完整版）
                    self.stats['commit_timeline'].append({
                        'date': date_str,
                        'time': dt.strftime('%H:%M'),
                        'timestamp': timestamp,
                        'author': author,
                        'subject': subject,
                        'is_merge': is_merge
                    })
                    
                    # 每日提交统计
                    self.stats['daily_commits'][date_str] += 1
                    
                    # 仓库首次和最后提交
                    if self.stats['first_commit_date'] is None or timestamp < self.stats['first_commit_date']:
                        self.stats['first_commit_date'] = timestamp
                    if self.stats['last_commit_date'] is None or timestamp > self.stats['last_commit_date']:
                        self.stats['last_commit_date'] = timestamp
                        
            elif current_commit and line.strip() and not line.startswith('COMMIT|'):
                # 解析文件变更统计
                parts = line.split('\t')
                if len(parts) >= 3:
                    try:
                        additions = int(parts[0]) if parts[0] != '-' else 0
                        deletions = int(parts[1]) if parts[1] != '-' else 0
                        filename = parts[2]
                        
                        current_commit['additions'] += additions
                        current_commit['deletions'] += deletions
                        current_commit['files'].append(filename)
                        
                        author = current_commit['author']
                        self.stats['authors'][author]['additions'] += additions
                        self.stats['authors'][author]['deletions'] += deletions
                        self.stats['authors'][author]['files_changed'].add(filename)
                    except (ValueError, IndexError):
                        pass
    
    def finalize_stats(self):
        """完成统计，计算衍生指标"""
        for author, data in self.stats['authors'].items():
            # 计算代码当量
            data['impact_score'] = self.calculate_impact_score(
                data['commits'],
                data['additions'],
                data['deletions']
            )
    
    def generate_html(self):
        """生成紧凑型 HTML 报告"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 准备数据
        authors_sorted = sorted(
            self.stats['authors'].items(),
            key=lambda x: x[1]['commits'],
            reverse=True
        )
        
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        # 生成作者选项（用于时间线筛选）
        author_options = ''
        for author, _ in authors_sorted:
            author_options += f'                            <option value="{author}">{author}</option>\n'
        
        # 生成作者行
        authors_rows = ''
        for idx, (author, data) in enumerate(authors_sorted[:20], 1):
            first_date = datetime.fromtimestamp(data['first_commit']).strftime('%Y-%m-%d') if data['first_commit'] else 'N/A'
            last_date = datetime.fromtimestamp(data['last_commit']).strftime('%Y-%m-%d') if data['last_commit'] else 'N/A'
            color = self.get_author_color(author)
            
            authors_rows += f"""                        <tr>
                            <td><span class="badge" style="background: {color};">#{idx}</span></td>
                            <td><strong>{author}</strong></td>
                            <td>{data['commits']}</td>
                            <td style="color: var(--success); font-weight: 600;">+{data['additions']:,}</td>
                            <td style="color: var(--danger); font-weight: 600;">-{data['deletions']:,}</td>
                            <td>{len(data['files_changed'])}</td>
                            <td><strong>{data['impact_score']:,}</strong></td>
                            <td style="font-size: 11px; color: #6b7280;">{first_date}</td>
                            <td style="font-size: 11px; color: #6b7280;">{last_date}</td>
                        </tr>
"""
        
        # 生成时间线（完整版，不限制数量）
        timeline_sorted = sorted(
            self.stats['commit_timeline'],
            key=lambda x: x['timestamp'],
            reverse=True
        )
        
        timeline_items = ''
        for commit in timeline_sorted:
            merge_class = ' merge' if commit.get('is_merge') else ''
            color = self.get_author_color(commit['author'])
            timeline_items += f"""                        <div class="timeline-item{merge_class}" style="border-left: 3px solid {color};">
                            <div class="timeline-date">{commit['date']} {commit.get('time', '')}</div>
                            <div class="timeline-author" style="color: {color};">{commit['author']}</div>
                            <div class="timeline-subject">{commit['subject'][:120]}</div>
                        </div>
"""
        
        # 生成小时分布条形图
        hour_data = [self.stats['by_hour'].get(h, 0) for h in range(24)]
        max_hour = max(hour_data) if hour_data and max(hour_data) > 0 else 1
        hour_bars = ''
        for hour in range(24):
            count = hour_data[hour]
            width = (count / max_hour * 100) if max_hour > 0 else 0
            hour_bars += f"""                            <div class="bar">
                                <div class="bar-label">{hour:02d}:00</div>
                                <div class="bar-track">
                                    <div class="bar-fill" style="width: {width}%">{count if count > 0 else ''}</div>
                                </div>
                            </div>
"""
        
        # 生成星期分布
        weekday_data = [self.stats['by_weekday'].get(d, 0) for d in range(7)]
        max_weekday = max(weekday_data) if weekday_data and max(weekday_data) > 0 else 1
        weekday_bars = ''
        for day in range(7):
            count = weekday_data[day]
            width = (count / max_weekday * 100) if max_weekday > 0 else 0
            weekday_bars += f"""                            <div class="bar">
                                <div class="bar-label">{weekday_names[day]}</div>
                                <div class="bar-track">
                                    <div class="bar-fill" style="width: {width}%">{count if count > 0 else ''}</div>
                                </div>
                            </div>
"""
        
        # 文件类型
        file_types_sorted = sorted(
            self.stats['file_types'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        max_files = max([count for _, count in file_types_sorted]) if file_types_sorted else 1
        filetype_bars = ''
        for ext, count in file_types_sorted:
            width = (count / max_files * 100) if max_files > 0 else 0
            display_ext = ext if ext != 'no-extension' else '无扩展名'
            filetype_bars += f"""                            <div class="bar">
                                <div class="bar-label">{display_ext}</div>
                                <div class="bar-track">
                                    <div class="bar-fill" style="width: {width}%">{count}</div>
                                </div>
                            </div>
"""
        
        # 月度趋势
        months_sorted = sorted(self.stats['by_month'].keys())
        month_commits = [self.stats['by_month'][m] for m in months_sorted]
        max_month = max(month_commits) if month_commits and max(month_commits) > 0 else 1
        month_bars = ''
        for month, count in zip(months_sorted[-12:], month_commits[-12:]):
            width = (count / max_month * 100) if max_month > 0 else 0
            month_bars += f"""                            <div class="bar">
                                <div class="bar-label">{month}</div>
                                <div class="bar-track">
                                    <div class="bar-fill" style="width: {width}%">{count if count > 0 else ''}</div>
                                </div>
                            </div>
"""
        
        # 获取模板并填充
        template = get_compact_html_template()
        html = template.format(
            repo_name=self.repo_name,
            generated_time=datetime.now().strftime('%Y-%m-%d %H:%M'),
            total_commits=self.stats['total_commits'],
            total_authors=len(self.stats['authors']),
            total_files=self.stats['total_files'],
            total_additions=sum(a['additions'] for a in self.stats['authors'].values()),
            authors_rows=authors_rows,
            author_options=author_options,
            timeline_items=timeline_items,
            hour_bars=hour_bars,
            weekday_bars=weekday_bars,
            filetype_bars=filetype_bars,
            month_bars=month_bars
        )
        
        # 写入文件
        output_file = os.path.join(self.output_dir, 'index.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ 报告已生成: {output_file}")

    def generate(self):
        """生成完整统计报告"""
        print(f"📊 正在分析仓库: {self.repo_name}")
        print(f"   路径: {self.repo_path}")
        
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            print(f"❌ 错误: {self.repo_path} 不是 Git 仓库")
            return False
        
        print("   收集基本信息...")
        self.collect_basic_info()
        
        print("   分析提交历史...")
        self.collect_commit_stats()
        
        print("   计算衍生指标...")
        self.finalize_stats()
        
        print("   生成 HTML 报告...")
        self.generate_html()
        
        return True


def main():
    if len(sys.argv) < 4:
        print("用法: python3 generate_stats.py <仓库路径> <输出目录> <仓库名称>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    output_dir = sys.argv[2]
    repo_name = sys.argv[3]
    
    generator = GitStatsGenerator(repo_path, output_dir, repo_name)
    success = generator.generate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
