import time
import random
from pymodbus.client.sync import ModbusTcpClient

# Modbus Server Configuration
PLC_IP = "localhost"  # Change if running on a different machine
PLC_PORT = 502

# Connect to OpenPLC Modbus Server
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
client.connect()

# Modbus Register Addresses for OpenPLC
TURBINE_RPM_REGISTER = 40001
GENERATOR_MW_REGISTER = 40002
GRID_DEMAND_REGISTER = 40003

# Simulation Loop
try:
    while True:
        # Generate Realistic Sensor Values
        turbine_rpm = random.randint(1800, 3200)  # Simulating actual turbine RPM range
        grid_demand = round(random.uniform(60.0, 120.0), 2)  # Power demand in MW

        # Adjust Generator Output Based on Turbine Speed
        generator_mw = grid_demand if turbine_rpm > 2000 else 0.0

        # Write to OpenPLC Modbus Registers
        client.write_register(TURBINE_RPM_REGISTER, turbine_rpm)
        client.write_register(GENERATOR_MW_REGISTER, int(generator_mw * 10))  # Scale MW for register
        client.write_register(GRID_DEMAND_REGISTER, int(grid_demand * 10))
        
        print(f"Turbine RPM: {turbine_rpm}, Generator MW: {generator_mw}, Grid Demand: {grid_demand}")
        time.sleep(5)  # Update every 5 seconds

except KeyboardInterrupt:
    print("Simulation stopped.")
    client.close()
