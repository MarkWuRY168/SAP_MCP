import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_handler import get_db_handler

def check_table_structure():
    """检查 tool_server 表结构"""
    db = get_db_handler()
    
    print("检查 tool_server 表结构...")
    print("=" * 80)
    
    try:
        with db.connection.cursor() as cursor:
            # 查看表结构
            cursor.execute("DESCRIBE tool_server")
            columns = cursor.fetchall()
            
            print("表结构:")
            for col in columns:
                print(f"  {col['Field']:20} {col['Type']:20} {col['Null']:5} {col['Key']:5} {col['Default']}")
            
            print("\n" + "=" * 80)
            
            # 查看表中的数据
            cursor.execute("SELECT * FROM tool_server LIMIT 5")
            rows = cursor.fetchall()
            
            print(f"表中共有 {len(rows)} 条记录:")
            for row in rows:
                print(f"\nID: {row.get('id')}")
                print(f"Name: {row.get('name')}")
                print(f"Description: {row.get('description')}")
                print(f"Category: {row.get('category')}")
                print(f"Is Active: {row.get('is_active')}")
                
                # 显示所有字段
                for key, value in row.items():
                    if key not in ['id', 'name', 'description', 'category', 'is_active']:
                        print(f"{key}: {value}")
                print("-" * 40)
                
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()