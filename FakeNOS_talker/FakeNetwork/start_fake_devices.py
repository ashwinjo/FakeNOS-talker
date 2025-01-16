from fakenos import FakeNOS
network_os = FakeNOS(inventory='/Users/ashwjosh/AgentUniverse/ReActAgent/NetworkAutomationAgent/FakeNetwork/inventory.yaml')
network_os.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    network_os.stop()