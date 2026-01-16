import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_handler import get_db_handler
import json

def check_database():
    """检查数据库中的工具数据"""
    db = get_db_handler()
    
    print("检查数据库中的工具数据...")
    print("=" * 80)
    
    # 获取所有工具
    tools = db.list_tools()
    
    print(f"数据库中共有 {len(tools)} 个工具:\n")
    
    for tool in tools:
        print(f"工具名称: {tool.get('name')}")
        print(f"描述: {tool.get('description')}")
        print(f"类别: {tool.get('category')}")
        print(f"是否激活: {tool.get('is_active')}")
        
        # 解析参数
        if tool.get('params'):
            try:
                params = json.loads(tool['params'])
                print(f"参数结构:")
                print(json.dumps(params, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"参数解析失败: {e}")
        
        print("-" * 80)
    
    # 测试获取特定工具
    print("\n测试获取特定工具: get_matnr_from_des")
    print("=" * 80)
    tool = db.get_tool("get_matnr_from_des")
    if tool:
        print("找到工具:")
        print(f"  名称: {tool.get('name')}")
        print(f"  描述: {tool.get('description')}")
        if tool.get('params'):
            params = json.loads(tool['params'])
            print(f"  参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
    else:
        print("未找到工具")

if __name__ == "__main__":
    check_database()