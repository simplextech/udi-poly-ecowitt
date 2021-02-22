#!/usr/bin/env python

try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

LOGGER = polyinterface.LOGGER


def lux_convert(wm2):
    lux = round(wm2 / 0.0079, 0)
    return lux


def ppm_convert(mg3):
    ppm = round(float(mg3) / 1000, 3)
    return ppm


def cardinal_direction(winddir):
    # Returns the Cardinal Direction Name
    if 0 <= winddir <= 11.24:
        return 1
    elif 11.25 <= winddir <= 33.74:
        return 2
    elif 33.75 <= winddir <= 56.24:
        return 3
    elif 56.25 <= winddir <= 78.74:
        return 4
    elif 78.75 <= winddir <= 101.24:
        return 5
    elif 101.25 <= winddir <= 123.74:
        return 6
    elif 123.75 <= winddir <= 146.24:
        return 7
    elif 146.25 <= winddir <= 168.74:
        return 8
    elif 168.75 <= winddir <= 191.24:
        return 9
    elif 191.25 <= winddir <= 213.74:
        return 10
    elif 213.75 <= winddir <= 236.24:
        return 11
    elif 236.25 <= winddir <= 258.74:
        return 12
    elif 258.75 <= winddir <= 281.24:
        return 13
    elif 281.25 <= winddir <= 303.74:
        return 14
    elif 303.75 <= winddir <= 326.24:
        return 15
    elif 326.25 <= winddir <= 348.74:
        return 16
    elif 348.75 <= winddir <= 360:
        return 1
    else:
        return 0


class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'EcoWitt Controller'
        self.sensors = []
        self.default_port = 8080
        self.debug = False

    def start(self):
        self.removeNoticesAll()
        LOGGER.info('Started EcoWitt NodeServer')
        self.check_params()
        httpd = HTTPServer(('', self.default_port), SimpleHTTPRequestHandler)
        httpd.serve_forever()
        # self.poly.add_custom_config_docs("<b>And this is some custom config data</b>")

    def shortPoll(self):
        pass

    def longPoll(self):
        pass

    def query(self):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        pass

    def delete(self):
        LOGGER.info('Removing EcoWitt Nodeserver')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config))
        LOGGER.info("process_config: Exit")

    def check_params(self):
        if 'port' in self.polyConfig['customParams']:
            self.default_port = int(self.polyConfig['customParams']['port'])
        self.addCustomParam({'port': self.default_port})

    def remove_notice_test(self,command):
        LOGGER.info('remove_notice_test: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNotice('test')

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def add_nodes(self, sensors):
        for k in sensors.keys():
            if self.debug == True:
                LOGGER.debug(k + ' : ' + sensors[k])
            
            '''
            Indoor Sensor Nodes
            '''
            if k == 'tempinf':
                ntype = 'indoor'
                if ntype not in self.nodes:
                    self.addNode(IndoorNode(self, self.address, 'indoor', 'Indoor'))
                else:
                    self.nodes['indoor'].setDriver('CLITEMP', sensors[k])
            if k == 'humidityin':
                ntype = 'indoor'
                if ntype not in self.nodes:
                    self.addNode(IndoorNode(self, self.address, 'indoor', 'Indoor'))
                else:
                    self.nodes['indoor'].setDriver('CLIHUM', sensors[k])
            '''
            Outdoor Sensor Nodes
            '''
            if k == 'tempf':
                ntype = 'outdoor'
                if ntype not in self.nodes:
                    self.addNode(OutdoorNode(self, self.address, 'outdoor', 'Outdoor'))
                else:
                    self.nodes['outdoor'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity':
                ntype = 'outdoor'
                if ntype not in self.nodes:
                    self.addNode(OutdoorNode(self, self.address, 'outdoor', 'Outdoor'))
                else:
                    self.nodes['outdoor'].setDriver('CLIHUM', sensors[k])
            if k == 'uv':
                ntype = 'outdoor'
                if ntype not in self.nodes:
                    self.addNode(OutdoorNode(self, self.address, 'outdoor', 'Outdoor'))
                else:
                    self.nodes['outdoor'].setDriver('UV', sensors[k])
            if k == 'solarradiation':
                ntype = 'outdoor'
                if ntype not in self.nodes:
                    self.addNode(OutdoorNode(self, self.address, 'outdoor', 'Outdoor'))
                else:
                    lux = lux_convert(float(sensors[k]))
                    self.nodes['outdoor'].setDriver('SOLRAD', sensors[k])
                    self.nodes['outdoor'].setDriver('LUMIN', lux)
            '''
            Pressure Sensor Node
            '''
            if k == 'baromabsin':
                ntype = 'pressure'
                if ntype not in self.nodes:
                    self.addNode(PressureNode(self, self.address, 'pressure', 'Pressure'))
                else:
                    self.nodes['pressure'].setDriver('ATMPRES', sensors[k])
            if k == 'baromrelin':
                ntype = 'pressure'
                if ntype not in self.nodes:
                    self.addNode(PressureNode(self, self.address, 'pressure', 'Pressure'))
                else:
                    self.nodes['pressure'].setDriver('BARPRES', sensors[k])
            '''
            Rain Sensor Node
            '''
            if k == 'hourlyrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV0', sensors[k])
            if k == 'dailyrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV1', sensors[k])
            if k == 'weeklyrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV2', sensors[k])
            if k == 'monthlyrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV3', sensors[k])
            if k == 'yearlyrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV4', sensors[k])
            if k == 'totalrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV5', sensors[k])
            if k == 'eventrainin':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV6', sensors[k])
            if k == 'rainratein':
                ntype = 'rain'
                if ntype not in self.nodes:
                    self.addNode(RainNode(self, self.address, 'rain', 'Rain'))
                else:
                    self.nodes['rain'].setDriver('GV7', sensors[k])
            '''
            Wind Sensor Node
            '''
            if k == 'winddir':
                ntype = 'wind'
                if ntype not in self.nodes:
                    self.addNode(WindNode(self, self.address, 'wind', 'Wind'))
                else:
                    cardinal = cardinal_direction(int(sensors[k]))
                    self.nodes['wind'].setDriver('WINDDIR', sensors[k])
                    self.nodes['wind'].setDriver('GV0', cardinal)
            if k == 'windgustmph':
                ntype = 'wind'
                if ntype not in self.nodes:
                    self.addNode(WindNode(self, self.address, 'wind', 'Wind'))
                else:
                    self.nodes['wind'].setDriver('GV1', sensors[k])
            if k == 'windspeedmph':
                ntype = 'wind'
                if ntype not in self.nodes:
                    self.addNode(WindNode(self, self.address, 'wind', 'Wind'))
                else:
                    self.nodes['wind'].setDriver('SPEED', sensors[k])
            if k == 'maxdailygust':
                ntype = 'wind'
                if ntype not in self.nodes:
                    self.addNode(WindNode(self, self.address, 'wind', 'Wind'))
                else:
                    self.nodes['wind'].setDriver('GV2', sensors[k])
            '''
            WH31 Sensor Node
            '''
            if k == 'temp1f':
                ntype = 'wh31_1'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_1', 'Sensor 1'))
                else:
                    self.nodes['wh31_1'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity1':
                ntype = 'wh31_1'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_1', 'Sensor 1'))
                else:
                    self.nodes['wh31_1'].setDriver('CLIHUM', sensors[k])
            if k == 'batt1':
                ntype = 'wh31_1'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_1', 'Sensor 1'))
                else:
                    self.nodes['wh31_1'].setDriver('BATLVL', sensors[k])
            if k == 'temp2f':
                ntype = 'wh31_2'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_2', 'Sensor 2'))
                else:
                    self.nodes['wh31_2'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity2':
                ntype = 'wh31_2'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_2', 'Sensor 2'))
                else:
                    self.nodes['wh31_2'].setDriver('CLIHUM', sensors[k])
            if k == 'batt2':
                ntype = 'wh31_2'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_2', 'Sensor 2'))
                else:
                    self.nodes['wh31_2'].setDriver('BATLVL', sensors[k])
            if k == 'temp3f':
                ntype = 'wh31_3'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_3', 'Sensor 3'))
                else:
                    self.nodes['wh31_3'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity3':
                ntype = 'wh31_3'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_3', 'Sensor 3'))
                else:
                    self.nodes['wh31_3'].setDriver('CLIHUM', sensors[k])
            if k == 'batt3':
                ntype = 'wh31_3'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_3', 'Sensor 3'))
                else:
                    self.nodes['wh31_3'].setDriver('BATLVL', sensors[k])
            if k == 'temp4f':
                ntype = 'wh31_4'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_4', 'Sensor 4'))
                else:
                    self.nodes['wh31_4'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity4':
                ntype = 'wh31_4'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_4', 'Sensor 4'))
                else:
                    self.nodes['wh31_4'].setDriver('CLIHUM', sensors[k])
            if k == 'batt4':
                ntype = 'wh31_4'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_4', 'Sensor 4'))
                else:
                    self.nodes['wh31_4'].setDriver('BATLVL', sensors[k])
            if k == 'temp5f':
                ntype = 'wh31_5'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_5', 'Sensor 5'))
                else:
                    self.nodes['wh31_5'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity5':
                ntype = 'wh31_5'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_5', 'Sensor 5'))
                else:
                    self.nodes['wh31_5'].setDriver('CLIHUM', sensors[k])
            if k == 'batt5':
                ntype = 'wh31_5'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_5', 'Sensor 5'))
                else:
                    self.nodes['wh31_5'].setDriver('BATLVL', sensors[k])
            if k == 'temp6f':
                ntype = 'wh31_6'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_6', 'Sensor 6'))
                else:
                    self.nodes['wh31_6'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity6':
                ntype = 'wh31_6'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_6', 'Sensor 6'))
                else:
                    self.nodes['wh31_6'].setDriver('CLIHUM', sensors[k])
            if k == 'batt6':
                ntype = 'wh31_6'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_6', 'Sensor 6'))
                else:
                    self.nodes['wh31_6'].setDriver('BATLVL', sensors[k])
            if k == 'temp7f':
                ntype = 'wh31_7'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_7', 'Sensor 7'))
                else:
                    self.nodes['wh31_7'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity7':
                ntype = 'wh31_7'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_7', 'Sensor 7'))
                else:
                    self.nodes['wh31_7'].setDriver('CLIHUM', sensors[k])
            if k == 'batt7':
                ntype = 'wh31_7'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_7', 'Sensor 7'))
                else:
                    self.nodes['wh31_7'].setDriver('BATLVL', sensors[k])
            if k == 'temp8f':
                ntype = 'wh31_8'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_8', 'Sensor 8'))
                else:
                    self.nodes['wh31_8'].setDriver('CLITEMP', sensors[k])
            if k == 'humidity8':
                ntype = 'wh31_8'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_8', 'Sensor 8'))
                else:
                    self.nodes['wh31_8'].setDriver('CLIHUM', sensors[k])
            if k == 'batt8':
                ntype = 'wh31_8'
                if ntype not in self.nodes:
                    self.addNode(WH31Node(self, self.address, 'wh31_8', 'Sensor 8'))
                else:
                    self.nodes['wh31_8'].setDriver('BATLVL', sensors[k])
            '''
            Soil Moisture Sensors
            '''
            if k == 'soilmoisture1':
                ntype = 'wh51_1'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_1', 'Soil 1'))
                else:
                    self.nodes['wh51_1'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt1' or k == 'Soilbatt1':
                ntype = 'wh51_1'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_1', 'Soil 1'))
                else:
                    self.nodes['wh51_1'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture2':
                ntype = 'wh51_2'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_2', 'Soil 2'))
                else:
                    self.nodes['wh51_2'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt2' or k == 'Soilbatt2':
                ntype = 'wh51_2'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_2', 'Soil 2'))
                else:
                    self.nodes['wh51_2'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture3':
                ntype = 'wh51_3'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_3', 'Soil 3'))
                else:
                    self.nodes['wh51_3'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt3' or k == 'Soilbatt3':
                ntype = 'wh51_3'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_3', 'Soil 3'))
                else:
                    self.nodes['wh51_3'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture4':
                ntype = 'wh51_4'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_4', 'Soil 4'))
                else:
                    self.nodes['wh51_4'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt4' or k == 'Soilbatt4':
                ntype = 'wh51_4'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_4', 'Soil 4'))
                else:
                    self.nodes['wh51_4'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture5':
                ntype = 'wh51_5'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_5', 'Soil 5'))
                else:
                    self.nodes['wh51_5'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt5' or k == 'Soilbatt5':
                ntype = 'wh51_5'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_5', 'Soil 5'))
                else:
                    self.nodes['wh51_5'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture6':
                ntype = 'wh51_6'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_6', 'Soil 6'))
                else:
                    self.nodes['wh51_6'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt6' or k == 'Soilbatt6':
                ntype = 'wh51_6'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_6', 'Soil 6'))
                else:
                    self.nodes['wh51_6'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture7':
                ntype = 'wh51_7'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_7', 'Soil 7'))
                else:
                    self.nodes['wh51_7'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt7' or k == 'Soilbatt7':
                ntype = 'wh51_7'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_7', 'Soil 7'))
                else:
                    self.nodes['wh51_7'].setDriver('BATLVL', sensors[k])
            if k == 'soilmoisture8':
                ntype = 'wh51_8'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_8', 'Soil 8'))
                else:
                    self.nodes['wh51_8'].setDriver('MOIST', sensors[k])
            if k == 'Siolbatt8' or k == 'Soilbatt8':
                ntype = 'wh51_8'
                if ntype not in self.nodes:
                    self.addNode(WH51Node(self, self.address, 'wh51_8', 'Soil 8'))
                else:
                    self.nodes['wh51_8'].setDriver('BATLVL', sensors[k])
            '''
            Air Quality Sensor
            '''
            if k == 'pm25_ch1':
                ntype = 'wh41_1'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_1', 'Air 1'))
                else:
                    self.nodes['wh41_1'].setDriver('GV0', ppm)
            if k == 'pm25batt1':
                ntype = 'wh41_1'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_1', 'Air 1'))
                else:
                    self.nodes['wh41_1'].setDriver('BATLVL', sensors[k])
            if k == 'pm25_ch2':
                ntype = 'wh41_2'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_2', 'Air 2'))
                else:
                    self.nodes['wh41_2'].setDriver('GV0', ppm)
            if k == 'pm25batt2':
                ntype = 'wh41_2'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_2', 'Air 2'))
                else:
                    self.nodes['wh41_2'].setDriver('BATLVL', sensors[k])
            if k == 'pm25_ch3':
                ntype = 'wh41_3'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_3', 'Air 3'))
                else:
                    self.nodes['wh41_3'].setDriver('GV0', ppm)
            if k == 'pm25batt3':
                ntype = 'wh41_3'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_3', 'Air 3'))
                else:
                    self.nodes['wh41_3'].setDriver('BATLVL', sensors[k])
            if k == 'pm25_ch4':
                ntype = 'wh41_4'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_4', 'Air 4'))
                else:
                    self.nodes['wh41_4'].setDriver('GV0', ppm)
            if k == 'pm25batt4':
                ntype = 'wh41_4'
                ppm = ppm_convert(sensors[k])
                if ntype not in self.nodes:
                    self.addNode(WH41Node(self, self.address, 'wh41_4', 'Air 4'))
                else:
                    self.nodes['wh41_4'].setDriver('BATLVL', sensors[k])

    id = 'controller'
    commands = {
        'QUERY': query,
        # 'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        # 'REMOVE_NOTICES_ALL': remove_notices_all,
        # 'REMOVE_NOTICE_TEST': remove_notice_test
    }
    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2}]


class IndoorNode(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(IndoorNode, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'CLITEMP', 'value': 0, 'uom': 17},
        {'driver': 'CLIHUM', 'value': 0, 'uom': 22}
    ]

    id = 'indoornode'

    commands = {
                    # 'DON': setOn, 'DOF': setOff
                }


class OutdoorNode(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(OutdoorNode, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'CLITEMP', 'value': 0, 'uom': 17},
        {'driver': 'CLIHUM', 'value': 0, 'uom': 22},
        {'driver': 'UV', 'value': 0, 'uom': 71},
        {'driver': 'SOLRAD', 'value': 0, 'uom': 74},
        {'driver': 'LUMIN', 'value': 0, 'uom': 36}
    ]

    id = 'outdoornode'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class PressureNode(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(PressureNode, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'BARPRES', 'value': 0, 'uom': 23},
        {'driver': 'ATMPRES', 'value': 0, 'uom': 23}
    ]

    id = 'pressurenode'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class RainNode(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(RainNode, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 0, 'uom': 105},  # Hourly Rain
        {'driver': 'GV1', 'value': 0, 'uom': 105},  # Daily Rain
        {'driver': 'GV2', 'value': 0, 'uom': 105},  # Weekly Rain
        {'driver': 'GV3', 'value': 0, 'uom': 105},  # Monthly Rain
        {'driver': 'GV4', 'value': 0, 'uom': 105},  # Yearly Rain
        {'driver': 'GV5', 'value': 0, 'uom': 105},  # Total Rain
        {'driver': 'GV6', 'value': 0, 'uom': 105},  # Event Rain
        {'driver': 'GV7', 'value': 0, 'uom': 105}  # Rain Rate
    ]

    id = 'rainnode'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class WindNode(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(WindNode, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'WINDDIR', 'value': 0, 'uom': 76},  # Wind Direction (degree)
        {'driver': 'GV0', 'value': 0, 'uom': 25},  # Wind Direction (cardinal)
        {'driver': 'SPEED', 'value': 0, 'uom': 48},  # Wind Speed
        {'driver': 'GV1', 'value': 0, 'uom': 48},  # Wind Gust
        {'driver': 'GV2', 'value': 0, 'uom': 48},  # Max Wind Gust Daily
    ]

    id = 'windnode'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class WH31Node(polyinterface.Node):
    def __init__(self, controller, primary, address, name):
        super(WH31Node, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'CLITEMP', 'value': 0, 'uom': 17},
        {'driver': 'CLIHUM', 'value': 0, 'uom': 22},
        {'driver': 'BATLVL', 'value': 0, 'uom': 25}
    ]

    id = 'wh31node'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class WH51Node(polyinterface.Node):
    # Soil Moisture Sensors
    def __init__(self, controller, primary, address, name):
        super(WH51Node, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'MOIST', 'value': 0, 'uom': 22},
        {'driver': 'BATLVL', 'value': 0, 'uom': 25}
    ]

    id = 'wh51node'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class WH41Node(polyinterface.Node):
    # Air Quality Sensors
    def __init__(self, controller, primary, address, name):
        super(WH41Node, self).__init__(controller, primary, address, name)

    def start(self):
        self.setDriver('ST', 1)
        pass

    def query(self):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    # hint = [1, 2, 3, 4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 0, 'uom': 54},
        {'driver': 'GV1', 'value': 0, 'uom': 54},
        {'driver': 'BATLVL', 'value': 0, 'uom': 25}
    ]

    id = 'wh41node'

    commands = {
        # 'DON': setOn, 'DOF': setOff
    }


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    LOGGER.info('Starting EcoWitt WebServer')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        # self.wfile.write(response.getvalue())
        # print(self.raw_requestline)
        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
            str(self.path), str(self.headers), body.decode('utf-8'))
        
        params = dict([p.split('=') for p in body.decode('utf-8').split('&')])
        control.add_nodes(params)


if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('EcoWitt')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
