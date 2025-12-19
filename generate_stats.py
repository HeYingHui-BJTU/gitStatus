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

class GitStatsGenerator:
    # 用户名到真实姓名的映射
    AUTHOR_MAPPING = {
        'Nahjs': '蒲显科',
        'QICY520': '曹棪',
        'YDUTSEVOLDN': '宁苏颜',
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
        """生成 HTML 报告"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 准备数据
        authors_sorted = sorted(
            self.stats['authors'].items(),
            key=lambda x: x[1]['commits'],
            reverse=True
        )
        
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        hour_data = [self.stats['by_hour'].get(h, 0) for h in range(24)]
        weekday_data = [self.stats['by_weekday'].get(d, 0) for d in range(7)]
        
        # 文件类型 Top 10
        file_types_sorted = sorted(
            self.stats['file_types'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # 月度提交趋势
        months_sorted = sorted(self.stats['by_month'].keys())
        month_commits = [self.stats['by_month'][m] for m in months_sorted]
        
        # 提交时间线（最近100条）
        timeline_sorted = sorted(
            self.stats['commit_timeline'],
            key=lambda x: x['timestamp'],
            reverse=True
        )[:100]
        
        # 生成 HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.repo_name} - 禾盈慧项目统计</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --info: #3b82f6;
            --dark: #1f2937;
            --light: #f9fafb;
            --border: #e5e7eb;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            overflow: hidden;
            animation: fadeIn 0.5s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Header Section */
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 15s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            50% {{ transform: translate(-10%, -10%) scale(1.1); }}
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        .brand {{
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.9;
            margin-bottom: 12px;
        }}
        
        .header h1 {{
            font-size: 42px;
            margin-bottom: 12px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            opacity: 0.95;
            font-size: 16px;
            margin-top: 8px;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 0;
            border-bottom: 1px solid var(--border);
        }}
        
        .stat-card {{
            background: white;
            padding: 32px 24px;
            text-align: center;
            border-right: 1px solid var(--border);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .stat-card:last-child {{
            border-right: none;
        }}
        
        .stat-card:hover {{
            background: var(--light);
            transform: translateY(-2px);
        }}
        
        .stat-card .icon {{
            font-size: 32px;
            margin-bottom: 12px;
        }}
        
        .stat-card .label {{
            font-size: 13px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        
        .stat-card .value {{
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Content Area */
        .content {{
            padding: 48px;
        }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 32px;
            transition: gap 0.3s ease;
        }}
        
        .back-link:hover {{
            gap: 12px;
        }}
        
        /* Section Styling */
        .section {{
            margin-bottom: 56px;
            animation: slideUp 0.5s ease-out;
        }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--border);
        }}
        
        .section-header h2 {{
            font-size: 28px;
            font-weight: 700;
            color: var(--dark);
            flex: 1;
        }}
        
        .section-header .icon {{
            font-size: 28px;
        }}
        
        /* Table Styling */
        .data-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        
        .data-table thead {{
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        }}
        
        .data-table th {{
            padding: 16px;
            text-align: left;
            font-weight: 600;
            color: #374151;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .data-table td {{
            padding: 16px;
            border-top: 1px solid var(--border);
        }}
        
        .data-table tbody tr {{
            transition: all 0.2s ease;
        }}
        
        .data-table tbody tr:hover {{
            background: #fafbfc;
            transform: scale(1.01);
        }}
        
        /* Chart Container */
        .chart-container {{
            background: linear-gradient(135deg, #fafbfc 0%, #f3f4f6 100%);
            border-radius: 16px;
            padding: 28px;
            margin: 20px 0;
            box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.06);
        }}
        
        .chart-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--dark);
        }}
        
        /* Bar Chart */
        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .bar {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .bar-label {{
            min-width: 90px;
            font-size: 14px;
            font-weight: 500;
            color: #4b5563;
        }}
        
        .bar-track {{
            flex: 1;
            height: 32px;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.06);
        }}
        
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 12px;
            color: white;
            font-size: 13px;
            font-weight: 700;
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            min-width: 40px;
        }}
        
        /* Badge */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            min-width: 32px;
            justify-content: center;
        }}
        
        .badge-success {{
            background: linear-gradient(135deg, #10b981, #059669);
        }}
        
        .badge-danger {{
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }}
        
        /* Timeline */
        .timeline {{
            position: relative;
            padding-left: 40px;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 12px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, var(--primary), var(--secondary));
        }}
        
        .timeline-item {{
            position: relative;
            margin-bottom: 24px;
            padding: 16px 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }}
        
        .timeline-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -28px;
            top: 24px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: 3px solid white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }}
        
        .timeline-date {{
            font-size: 12px;
            color: #6b7280;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        
        .timeline-author {{
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 6px;
        }}
        
        .timeline-subject {{
            font-size: 14px;
            color: #4b5563;
            line-height: 1.5;
        }}
        
        /* Scrollbar Styling */
        .timeline::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .timeline::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        .timeline::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 4px;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .content {{
                padding: 24px;
            }}
            .header {{
                padding: 40px 24px;
            }}
            .header h1 {{
                font-size: 32px;
            }}
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            .stat-card {{
                border-right: none;
                border-bottom: 1px solid var(--border);
            }}
            .stat-card:last-child {{
                border-bottom: none;
            }}
            .bar-label {{
                min-width: 60px;
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <div class="brand">禾盈慧 • HeYingHui</div>
                <h1>{self.repo_name}</h1>
                <p class="subtitle">Git 仓库协作统计分析报告</p>
                <p class="subtitle" style="margin-top: 4px; font-size: 14px;">生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📝</div>
                <div class="label">总提交数</div>
                <div class="value">{self.stats['total_commits']}</div>
            </div>
            <div class="stat-card">
                <div class="icon">👥</div>
                <div class="label">贡献者</div>
                <div class="value">{len(self.stats['authors'])}</div>
            </div>
            <div class="stat-card">
                <div class="icon">📁</div>
                <div class="label">文件总数</div>
                <div class="value">{self.stats['total_files']}</div>
            </div>
            <div class="stat-card">
                <div class="icon">✨</div>
                <div class="label">代码变更</div>
                <div class="value">{sum(a['additions'] for a in self.stats['authors'].values()):,}</div>
            </div>
        </div>
        
        <div class="content">
            <a href="../index.html" class="back-link">
                <span>←</span>
                <span>返回总门户</span>
            </a>
            
            <div class="section">
                <div class="section-header">
                    <span class="icon">👥</span>
                    <h2>贡献者排行榜</h2>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th style="width: 60px;">排名</th>
                            <th>贡献者</th>
                            <th style="width: 100px;">提交次数</th>
                            <th style="width: 100px;">新增行数</th>
                            <th style="width: 100px;">删除行数</th>
                            <th style="width: 100px;">修改文件</th>
                            <th style="width: 120px;">首次提交</th>
                            <th style="width: 120px;">最后提交</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        for idx, (author, data) in enumerate(authors_sorted[:20], 1):
            first_date = datetime.fromtimestamp(data['first_commit']).strftime('%Y-%m-%d') if data['first_commit'] else 'N/A'
            last_date = datetime.fromtimestamp(data['last_commit']).strftime('%Y-%m-%d') if data['last_commit'] else 'N/A'
            
            html += f"""                        <tr>
                            <td><span class="badge">#{idx}</span></td>
                            <td><strong style="color: var(--dark);">{author}</strong></td>
                            <td><strong>{data['commits']}</strong></td>
                            <td><span class="badge-success" style="display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">+{data['additions']:,}</span></td>
                            <td><span class="badge-danger" style="display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">-{data['deletions']:,}</span></td>
                            <td>{len(data['files_changed'])}</td>
                            <td style="color: #6b7280; font-size: 13px;">{first_date}</td>
                            <td style="color: #6b7280; font-size: 13px;">{last_date}</td>
                        </tr>
"""
        
        html += """                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <span class="icon">📅</span>
                    <h2>提交历史时间线</h2>
                </div>
                <div class="timeline">
"""
        
        for commit in timeline_sorted[:50]:
            html += f"""                    <div class="timeline-item">
                        <div class="timeline-date">{commit['date']} {datetime.fromtimestamp(commit['timestamp']).strftime('%H:%M')}</div>
                        <div class="timeline-author">{commit['author']}</div>
                        <div class="timeline-subject">{commit['subject']}</div>
                    </div>
"""
        
        html += """                </div>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <span class="icon">⏰</span>
                    <h2>活跃时段分析</h2>
                </div>
                <div class="chart-container">
                    <div class="chart-title">按小时分布</div>
                    <div class="bar-chart">
"""
        
        max_hour = max(hour_data) if hour_data and max(hour_data) > 0 else 1
        for hour in range(24):
            count = hour_data[hour]
            width = (count / max_hour * 100) if max_hour > 0 else 0
            html += f"""                        <div class="bar">
                            <div class="bar-label">{hour:02d}:00</div>
                            <div class="bar-track">
                                <div class="bar-fill" style="width: {width}%">{count if count > 0 else ''}</div>
                            </div>
                        </div>
"""
        
        html += """                    </div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">按星期分布</div>
                    <div class="bar-chart">
"""
        
        max_weekday = max(weekday_data) if weekday_data and max(weekday_data) > 0 else 1
        for day in range(7):
            count = weekday_data[day]
            width = (count / max_weekday * 100) if max_weekday > 0 else 0
            html += f"""                        <div class="bar">
                            <div class="bar-label">{weekday_names[day]}</div>
                            <div class="bar-track">
                                <div class="bar-fill" style="width: {width}%">{count if count > 0 else ''}</div>
                            </div>
                        </div>
"""
        
        html += """                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <span class="icon">📁</span>
                    <h2>文件类型分布</h2>
                </div>
                <div class="chart-container">
                    <div class="chart-title">Top 10 文件类型</div>
                    <div class="bar-chart">
"""
        
        max_files = max([count for _, count in file_types_sorted]) if file_types_sorted else 1
        for ext, count in file_types_sorted:
            width = (count / max_files * 100) if max_files > 0 else 0
            display_ext = ext if ext != 'no-extension' else '无扩展名'
            html += f"""                        <div class="bar">
                            <div class="bar-label">{display_ext}</div>
                            <div class="bar-track">
                                <div class="bar-fill" style="width: {width}%">{count}</div>
                            </div>
                        </div>
"""
        
        html += """                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <span class="icon">📈</span>
                    <h2>月度提交趋势</h2>
                </div>
                <div class="chart-container">
                    <div class="chart-title">最近12个月提交活跃度</div>
                    <div class="bar-chart">
"""
        
        max_month = max(month_commits) if month_commits and max(month_commits) > 0 else 1
        for month, count in zip(months_sorted[-12:], month_commits[-12:]):
            width = (count / max_month * 100) if max_month > 0 else 0
            html += f"""                        <div class="bar">
                            <div class="bar-label">{month}</div>
                            <div class="bar-track">
                                <div class="bar-fill" style="width: {width}%">{count if count > 0 else ''}</div>
                            </div>
                        </div>
"""
        
        html += """                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 添加平滑滚动和加载动画
        document.addEventListener('DOMContentLoaded', function() {{
            // 为表格行添加延迟动画
            const rows = document.querySelectorAll('.data-table tbody tr');
            rows.forEach((row, index) => {{
                row.style.animation = `slideUp 0.3s ease-out ${{index * 0.05}}s both`;
            }});
            
            // 为条形图添加延迟动画
            const bars = document.querySelectorAll('.bar-fill');
            bars.forEach((bar, index) => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100 + index * 30);
            }});
        }});
    </script>
</body>
</html>
"""
        
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
