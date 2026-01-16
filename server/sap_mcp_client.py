import asyncio
import json
import os
import sys

from fastmcp import Client

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MCP_SERVER_CONFIG

client = Client(f"http://{MCP_SERVER_CONFIG['host']}:{MCP_SERVER_CONFIG['port']}{MCP_SERVER_CONFIG['path']}")

async def get_tool_list():
    """获取工具清单"""
    async with client:
        result = await client.call_tool("get_tool_list", {})
        print("=" * 80)
        print("1. 获取工具清单:")
        print("=" * 80)
        
        if hasattr(result, 'data'):
            data = result.data
        else:
            data = result
        
        # 处理 JSONRPC 格式的响应
        if isinstance(data, dict) and "RESULT" in data:
            data = data["RESULT"]
        
        if isinstance(data, list):
            for tool in data:
                print(f"  TOOL_ID: {tool.get('TOOL_ID')}")
                print(f"  DESCRIPTION: {tool.get('DESCRIPTION')}")
                print("-" * 40)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        
        return data

async def get_tool_details(tool_id: str):
    """获取工具详情
    
    Args:
        tool_id: 工具ID
    """
    async with client:
        json_data = {
            "TOOL_ID": tool_id
        }
        result = await client.call_tool("get_tool_details", {"json_data": json_data})
        print("=" * 80)
        print(f"2. 获取工具详情 (TOOL_ID: {tool_id}):")
        print("=" * 80)
        
        if hasattr(result, 'data'):
            data = result.data
        else:
            data = result
        
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data

async def use_tool(tool_id: str, params: dict):
    """使用工具
    
    Args:
        tool_id: 工具ID
        params: 工具参数（简化格式，直接传参数名和值）
    """
    async with client:
        json_data = {
            "TOOL_ID": tool_id,
            **params
        }
        
        result = await client.call_tool("use_tool", {"json_data": json_data})
        print("=" * 80)
        print(f"3. 使用工具 (TOOL_ID: {tool_id}):")
        print("=" * 80)
        print(f"传入参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
        print("-" * 80)
        
        if hasattr(result, 'data'):
            data = result.data
        else:
            data = result
        
        print("执行结果:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data

async def test_complete_flow():
    """完整的测试流程"""
    print("\n" + "=" * 80)
    print("开始测试 SAP MCP Server")
    print("=" * 80 + "\n")
    
    try:
        # 步骤1: 获取工具清单
        print("\n步骤1: 获取工具清单\n")
        tool_list = await get_tool_list()
        
        if not tool_list or not isinstance(tool_list, list):
            print("错误: 无法获取工具清单")
            return
        
        # 选择一个工具进行测试
        # 使用 get_matnr_from_des 作为测试工具
        test_tool_id = "get_matnr_from_des"
        print(f"\n选择工具进行测试: {test_tool_id}")
        
        # 步骤2: 获取工具详情（这会将参数格式保存到数据库）
        print("\n步骤2: 获取工具详情\n")
        tool_details = await get_tool_details(test_tool_id)
        
        if not tool_details:
            print("错误: 无法获取工具详情")
            return
        
        # 步骤3: 使用工具
        print("\n步骤3: 使用工具\n")
        
        # 根据接口文档，get_matnr_from_des 需要以下参数:
        # LANGU: 语言类型 (如 "ZH")
        # MAKTX: 物料描述
        test_params = {
            "LANGU": "ZH",
            "MAKTX": "125ml35度中国劲酒（JING版2020）_1*24"
        }
        
        result = await use_tool(test_tool_id, test_params)
        
        # 检查结果
        if result and isinstance(result, dict):
            if "error" in result:
                print(f"\n错误: {result['error']}")
            else:
                print("\n测试成功！")
        else:
            print("\n测试完成")
            
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    await test_complete_flow()

if __name__ == "__main__":
    asyncio.run(main())
