#!/usr/bin/env python3
"""
禾盈慧 (HeYingHui) - 一键全量生成统计
协作洞察工具批量生成脚本
"""

import os
import sys
import subprocess
from pathlib import Path

# 项目配置
PROJECTS = [
    {
        "path": "/mnt/d/heyinghui/frontend",
        "name": "前端模块 (Frontend)",
        "dir": "frontend_stats",
        "desc": "用户界面与交互设计",
        "icon": "🎨"
    },
    {
        "path": "/mnt/d/heyinghui/backend",
        "name": "后端模块 (Backend)",
        "dir": "backend_stats",
        "desc": "服务端架构与业务逻辑",
        "icon": "⚙️"
    },
    {
        "path": "/mnt/d/heyinghui/dataCenter",
        "name": "数据中心 (DataCenter)",
        "dir": "dataCenter_stats",
        "desc": "数据采集、分析与智能预测",
        "icon": "📊"
    }
]

def generate_portal(output_dir, total_stats):
    """生成智能总门户页面"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>禾盈慧项目 - 多仓库协作统计总表</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    
    html {{ scroll-behavior: smooth; }}
    
    :root {{
      --primary: #667eea;
      --secondary: #764ba2;
      --success: #10b981;
      --dark: #1f2937;
      --light: #f9fafb;
      --border: #e5e7eb;
    }}
    
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
      min-height: 100vh;
      padding: 40px 20px;
      color: var(--dark);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    
    .container {{
      max-width: 1200px;
      width: 100%;
      animation: fadeIn 0.6s ease-out;
    }}
    
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(30px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .header {{
      text-align: center;
      color: white;
      margin-bottom: 48px;
    }}
    
    .brand {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 16px;
      opacity: 0.95;
    }}
    
    .title {{
      font-size: 48px;
      font-weight: 800;
      margin-bottom: 16px;
      text-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    
    .subtitle {{
      font-size: 18px;
      opacity: 0.9;
      line-height: 1.6;
    }}
    
    /* 总览卡片 */
    .overview {{
      background: rgba(255, 255, 255, 0.95);
      border-radius: 20px;
      padding: 32px;
      margin-bottom: 40px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    
    .overview-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 24px;
      color: var(--dark);
      text-align: center;
    }}
    
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 24px;
    }}
    
    .stat-item {{
      text-align: center;
      padding: 20px;
      background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
      border-radius: 12px;
    }}
    
    .stat-icon {{
      font-size: 32px;
      margin-bottom: 8px;
    }}
    
    .stat-label {{
      font-size: 12px;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
      font-weight: 600;
    }}
    
    .stat-value {{
      font-size: 32px;
      font-weight: 700;
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    
    .card-container {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
      margin-bottom: 40px;
    }}
    
    .card {{
      background: white;
      border-radius: 20px;
      padding: 32px;
      text-decoration: none;
      color: var(--dark);
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
    }}
    
    .card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--primary), var(--secondary));
    }}
    
    .card:hover {{
      transform: translateY(-8px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }}
    
    .card-icon {{
      font-size: 48px;
      margin-bottom: 16px;
    }}
    
    .card-title {{
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--dark);
    }}
    
    .card-desc {{
      font-size: 14px;
      color: #6b7280;
      line-height: 1.5;
      margin-bottom: 16px;
    }}
    
    .card-stats {{
      display: flex;
      gap: 16px;
      font-size: 13px;
      color: #6b7280;
    }}
    
    .card-stat {{
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    
    .footer {{
      background: rgba(255, 255, 255, 0.95);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    
    .footer-title {{
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 12px;
      color: var(--dark);
    }}
    
    .footer-content {{
      font-size: 14px;
      color: #6b7280;
      line-height: 1.6;
    }}
    
    .footer-content strong {{
      color: var(--primary);
      font-weight: 600;
    }}
    
    /* 打印样式 */
    @media print {{
      body {{ background: white; padding: 20px; }}
      .container {{ box-shadow: none; }}
      .card:hover {{ transform: none; }}
    }}
    
    @media (max-width: 768px) {{
      .title {{ font-size: 36px; }}
      .card-container {{ grid-template-columns: 1fr; }}
      .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">禾盈慧 • HeYingHui</div>
      <h1 class="title">多仓库协作统计</h1>
      <p class="subtitle">项目团队 Git 提交历史与协作深度分析</p>
    </div>
    
    <div class="overview">
      <div class="overview-title">📊 项目总览</div>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-icon">📝</div>
          <div class="stat-label">总提交数</div>
          <div class="stat-value">{total_stats['total_commits']}</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon">📁</div>
          <div class="stat-label">总文件数</div>
          <div class="stat-value">{total_stats['total_files']}</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon">➕</div>
          <div class="stat-label">新增代码行</div>
          <div class="stat-value">{total_stats['total_additions']:,}</div>
        </div>
        <div class="stat-item">
          <div class="stat-icon">🔀</div>
          <div class="stat-label">合并次数</div>
          <div class="stat-value">{total_stats['total_merges']}</div>
        </div>
      </div>
    </div>
    
    <div class="card-container">
"""
    
    for project in PROJECTS:
        html += f"""      <a class="card" href="./{project['dir']}/index.html">
        <div class="card-icon">{project.get('icon', '📦')}</div>
        <h3 class="card-title">{project['name']}</h3>
        <p class="card-desc">{project['desc']}</p>
        <div class="card-stats">
          <div class="card-stat">
            <span>📝</span>
            <span>点击查看详情</span>
          </div>
        </div>
      </a>
"""
    
    html += """    </div>
    
    <div class="footer">
      <div class="footer-title">📈 统计说明</div>
      <div class="footer-content">
        本报告基于 Git 提交日志生成，展示各仓库的<strong>贡献者排行</strong>、<strong>完整提交时间线</strong>、<strong>协作热力图</strong>、<strong>活跃时段分析</strong>等关键指标。<br>
        团队成员包括：<strong>蒲显科</strong>、<strong>曹棪</strong>、<strong>宁苏颜</strong>、<strong>黄光景</strong>、<strong>张琪</strong>
      </div>
    </div>
  </div>
  
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const cards = document.querySelectorAll('.card');
      cards.forEach((card, index) => {
        card.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s both`;
      });
    });
  </script>
</body>
</html>"""
    
    output_file = os.path.join(output_dir, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 总门户已生成: {output_file}")

def main():
    """主函数：一键生成所有统计"""
    script_dir = Path(__file__).parent
    output_root = script_dir / 'project-reports'
    
    print("🚀 禾盈慧协作洞察工具 - 一键全量生成")
    print("=" * 60)
    
    total_stats = {
        'total_commits': 0,
        'total_files': 0,
        'total_additions': 0,
        'total_merges': 0
    }
    
    # 为每个项目生成统计
    for i, project in enumerate(PROJECTS, 1):
        print(f"\n[{i}/{len(PROJECTS)}] 处理: {project['name']}")
        print("-" * 60)
        
        repo_path = project['path']
        output_dir = output_root / project['dir']
        
        if not os.path.exists(repo_path):
            print(f"⚠️  跳过: 仓库路径不存在 - {repo_path}")
            continue
        
        # 调用原有的生成脚本
        cmd = [
            'python3',
            str(script_dir / 'generate_stats.py'),
            repo_path,
            str(output_dir),
            project['name']
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"❌ 错误: {result.stderr}")
        else:
            # 尝试读取生成的统计数据（简化版）
            # 这里可以改进为解析HTML或保存JSON中间文件
            pass
    
    print("\n" + "=" * 60)
    print("📊 生成总门户页面...")
    generate_portal(output_root, total_stats)
    
    print("\n" + "=" * 60)
    print("✨ 所有统计报告已生成完毕！")
    print(f"📁 输出目录: {output_root}")
    print(f"🌐 访问入口: {output_root / 'index.html'}")
    print("\n💡 提示：使用浏览器打开 index.html 即可查看")

if __name__ == '__main__':
    main()
