from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool(name="greet")
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000, path="/mcp")  # 使用 HTTP 传输方式，匹配客户端配置