# https://discord.gg/Z34hwhSPBk
# Discord: aidsplus

import requests
import time
from valclient import Client


class ValorantAPI:
    def init(self):
        self.client = Client()
        self.agent_dict = self.get_agents()

    def get_agents(self):
        response = requests.get("https://valorant-api.com/v1/agents")
        if response.status_code != 200:
            print("Erro ao acessar valorant-api.com")
            time.sleep(3)
            exit(0)

        agents = response.json()['data']
        agent_dict = {}
        for agent in agents:
            if not agent['isPlayableCharacter']:
                continue
            agent_dict[agent['displayName'].lower()] = agent['uuid']
        return agent_dict

    def activate_client(self):
        try:
            self.client.activate()
            local = self.client.fetch(endpoint="/riotclient/region-locale", endpoint_type="local")
            print("Resposta da API:", local)

            api_region = local.get('region', '').lower()
            region_mapping = {
                'na': 'na',
                'eu': 'eu',
                'latam': 'latam',
                'br': 'br',
                'ap': 'ap',
                'kr': 'kr',
                'eune': 'eu',
                'pbe': 'pbe',
            }

            if api_region in region_mapping:
                self.client = Client(region=region_mapping[api_region])
                self.client.activate()
            else:
                raise ValueError(f"Região inválida retornada da API Valorant. Regiões disponíveis: {list(region_mapping.values())}")

        except Exception as e:
            print(f"Valorant não rodando: {e}")
            time.sleep(3)
            exit(0)

    def select_agent(self, agent_name):
        agent_name = agent_name.lower()
        uuid = self.agent_dict.get(agent_name, '')
        if uuid == '':
            print("Nome do agente inválido")
            time.sleep(3)
            exit(0)

        print(uuid)
        while self.client.session_fetch()['loopState'] != "PREGAME":
            time.sleep(0.01)

        self.client.pregame_select_character(uuid)
        self.client.pregame_lock_character(uuid)


if __name__ == "__main__":
    valorant_api = ValorantAPI()
    valorant_api.activate_client()
    agente = input("Agente: ")
    valorant_api.select_agent(agente)
