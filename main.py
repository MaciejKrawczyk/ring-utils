import json
# order_json_file


class StelmachMetrixOrder:

    def __init__(self, json_file):
        with open(f'{json_file}') as order_json_file:
            global json_data
            json_data = json.load(order_json_file)
            self.json_data = json_data

    def get_profile(self):
        return json_data['profile']['profileId']

    def get_diameter_mm(self):
        return json_data['common']['diameter']

    def get_ring_parameters(self):
        r50 = json_data['common']['size']
        r51 = json_data['profile']['shank']['width']
        r52 = json_data['profile']['shank']['height']
        r60 = json_data['profile']['shank']['parts']['inner']['radius']
        r40 = json_data['profile']['shank']['parts']['inner']['edge']['size']
        r61 = json_data['profile']['shank']['parts']['outer']['radius']
        r41 = json_data['profile']['shank']['parts']['outer']['edge']['size']
        if json_data['profile']['shank']['parts']['outer']['edge']['type'] == 'bevel':
            r20 = json_data['profile']['shank']['parts']['inner']['edge']['size']
            r40 = 0
        else:
            r40 = json_data['profile']['shank']['parts']['inner']['edge']['size']
            r20 = 0
        return {'r50': r50, 'r51': r51, "r52": r52,
                'r60': r60, 'r40': r40, 'r61': r61,
                'r41': r41, 'r20': r20}

    def get_grooves(self):
        grooves = json_data['profile']['grooves']
        print(f'number of grooves: {len(grooves)}')
        grooves_dict = {}
        for i, groove in enumerate(grooves):
            grooves_dict[f'groove_{i+1}'] = groove
        return grooves_dict

    def get_edges(self):
        edges = json_data['profile']['edges']
        print(f'number of edges: {len(edges)}')
        edges_dict = {}
        for i, edge in enumerate(edges):
            edges[f'edge_{i + 1}'] = edge
        return edges_dict

    def get_stones(self):
        stones = json_data['profile']['stoneLayout']
        return stones



order = StelmachMetrixOrder("json-files/572701-FP-U34P-73BX.json")
print(order.get_ring_parameters())
print(order.get_grooves())
print(order.get_edges())
print(order.get_diameter_mm())
print(order.get_stones())
