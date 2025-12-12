from mcp.server.fastmcp import FastMCP
# Create an instance of FastMCP 
# All parameters are optional 
mcp = FastMCP( 
name="MyCalculator" 
) 
# Define a simple addition tool
@mcp.tool() 
def add(a: float, b: float) -> float: 
    """Returns the sum of two numbers.""" 
    return a + b 
 
 
@mcp.tool() 
def subtract(a: float, b: float) -> float: 
    """ Subtracts b from a and returns the result""" 
    return a - b 
 
 
@mcp.tool() 
def multiply(a: float, b: float) -> float: 
    """ Multiplies two numbers and returns the result """ 
    return a * b 
 
 
@mcp.tool() 
def divide(a: float, b: float) -> float: 
    """ Divides a by b and returns the result """ 
    if b == 0: 
        raise ValueError("Cannot divide by zero") 
    return a / b 
 
if __name__ == "__main__": 
    mcp.run(transport="http") 
    # You can change transport to "sse" if needed 