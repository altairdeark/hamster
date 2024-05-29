import requests
import json
import sys


# URL для запроса
url = "https://api.hamsterkombat.io/clicker/upgrades-for-buy"

# Ваш Bearer токен
bearer_token = "token"

# Заголовки для запроса
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}


def get_current_balance():
    response = requests.post("https://api.hamsterkombat.io/clicker/sync", headers=headers, json={})
    if response.status_code == 200:
        data = response.json()
        return data.get("clickerUser").get("balanceCoins")
    return 0

# Данные для POST запроса (если необходимы)
payload = {}  # если нет необходимости передавать данные, оставьте пустым


current_balance = get_current_balance()
# Выполнение POST запроса
response = requests.post(url, headers=headers, json=payload)

# Проверка статуса ответа
if response.status_code == 200:
    # Парсинг JSON данных
    data = response.json()
    
    # Извлечение имен элементов и вычисление показателя выгоды
    upgrades = []
    for upgrade in data.get("upgradesForBuy", []):
        name = upgrade.get("name")
        price = upgrade.get("price")
        profit_per_hour_delta = upgrade.get("profitPerHourDelta")
        if upgrade.get("isAvailable") == False or upgrade.get("isExpired") == True:
            continue
        if upgrade.get("cooldownSeconds") != None and upgrade.get("cooldownSeconds") > 0:
            continue
        if price > current_balance:
            continue
        benefit = price / profit_per_hour_delta if profit_per_hour_delta != 0 else float('inf')
        
        upgrades.append((name, benefit, upgrade.get("level")))  # сохраняем имя элемента и его показатель выгоды
    
    # Сортировка по показателю выгоды
    sorted_upgrades = sorted(upgrades, key=lambda x: x[1])  # сортировка по второму элементу кортежа (показатель выгоды)
    
    # Вывод отсортированных имен элементов
    if len(sorted_upgrades) == 0:
        print("Not found")
        sys.exit(0)
    print(f'{sorted_upgrades[0][0]} - {sorted_upgrades[0][2]}lvl: Profit {sorted_upgrades[0][1]}')
    if len(sorted_upgrades) > 1:
        print(f'{sorted_upgrades[1][0]} - {sorted_upgrades[1][2]}lvl: Profit {sorted_upgrades[1][1]}')
    if len(sorted_upgrades) > 2:
        print(f'{sorted_upgrades[2][0]} - {sorted_upgrades[2][2]}lvl: Profit {sorted_upgrades[2][1]}')
    
    # for name, profit, level in sorted_upgrades:
        # print(f'{name} - {level}lvl: Profit {profit}')
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
