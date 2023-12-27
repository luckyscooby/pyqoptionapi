"""Module for IQ option websocket."""

import json
import logging
import websocket
import pyqoptionapi.constants as OP_code
import pyqoptionapi.global_value as global_value
from threading import Thread
from pyqoptionapi.ws.received.technical_indicators import technical_indicators
from pyqoptionapi.ws.received.time_sync import time_sync
from pyqoptionapi.ws.received.heartbeat import heartbeat
from pyqoptionapi.ws.received.balances import balances
from pyqoptionapi.ws.received.profile import profile
from pyqoptionapi.ws.received.balance_changed import balance_changed
from pyqoptionapi.ws.received.candles import candles
from pyqoptionapi.ws.received.buy_complete import buy_complete
from pyqoptionapi.ws.received.option import option
from pyqoptionapi.ws.received.position_history import position_history
from pyqoptionapi.ws.received.list_info_data import list_info_data
from pyqoptionapi.ws.received.candle_generated import candle_generated_realtime
from pyqoptionapi.ws.received.candle_generated_v2 import candle_generated_v2
from pyqoptionapi.ws.received.commission_changed import commission_changed
from pyqoptionapi.ws.received.socket_option_opened import socket_option_opened
from pyqoptionapi.ws.received.api_option_init_all_result import api_option_init_all_result
from pyqoptionapi.ws.received.initialization_data import initialization_data
from pyqoptionapi.ws.received.underlying_list import underlying_list
from pyqoptionapi.ws.received.instruments import instruments
from pyqoptionapi.ws.received.financial_information import financial_information
from pyqoptionapi.ws.received.position_changed import position_changed
from pyqoptionapi.ws.received.option_opened import option_opened
from pyqoptionapi.ws.received.option_closed import option_closed
from pyqoptionapi.ws.received.top_assets_updated import top_assets_updated
from pyqoptionapi.ws.received.strike_list import strike_list
from pyqoptionapi.ws.received.api_game_betinfo_result import api_game_betinfo_result
from pyqoptionapi.ws.received.traders_mood_changed import traders_mood_changed
from pyqoptionapi.ws.received.order import order
from pyqoptionapi.ws.received.position import position
from pyqoptionapi.ws.received.positions import positions
from pyqoptionapi.ws.received.order_placed_temp import order_placed_temp
from pyqoptionapi.ws.received.deferred_orders import deferred_orders
from pyqoptionapi.ws.received.history_positions import history_positions
from pyqoptionapi.ws.received.available_leverages import available_leverages
from pyqoptionapi.ws.received.order_canceled import order_canceled
from pyqoptionapi.ws.received.position_closed import position_closed
from pyqoptionapi.ws.received.overnight_fee import overnight_fee
from pyqoptionapi.ws.received.api_game_getoptions_result import api_game_getoptions_result
from pyqoptionapi.ws.received.sold_options import sold_options
from pyqoptionapi.ws.received.tpsl_changed import tpsl_changed
from pyqoptionapi.ws.received.auto_margin_call_changed import auto_margin_call_changed
from pyqoptionapi.ws.received.digital_option_placed import digital_option_placed
from pyqoptionapi.ws.received.result import result
from pyqoptionapi.ws.received.instrument_quotes_generated import instrument_quotes_generated
from pyqoptionapi.ws.received.training_balance_reset import training_balance_reset
from pyqoptionapi.ws.received.socket_option_closed import socket_option_closed
from pyqoptionapi.ws.received.live_deal_binary_option_placed import live_deal_binary_option_placed
from pyqoptionapi.ws.received.live_deal_digital_option import live_deal_digital_option
from pyqoptionapi.ws.received.leaderboard_deals_client import leaderboard_deals_client
from pyqoptionapi.ws.received.live_deal import live_deal
from pyqoptionapi.ws.received.user_profile_client import user_profile_client
from pyqoptionapi.ws.received.leaderboard_userinfo_deals_client import leaderboard_userinfo_deals_client
from pyqoptionapi.ws.received.client_price_generated import client_price_generated
from pyqoptionapi.ws.received.users_availability import users_availability


class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)

    def dict_queue_add(self, dict, maxdict, key1, key2, key3, value):
        if key3 in dict[key1][key2]:
            dict[key1][key2][key3] = value
        else:
            while True:
                try:
                    dic_size = len(dict[key1][key2])
                except:
                    dic_size = 0
                if dic_size < maxdict:
                    dict[key1][key2][key3] = value
                    break
                else:
                    # del mini key
                    del dict[key1][key2][sorted(
                        dict[key1][key2].keys(), reverse=False)[0]]

    def api_dict_clean(self, obj):
        if len(obj) > 5000:
            for k in obj.keys():
                del obj[k]
                break

    def on_message(self, _, message):  # pylint: disable=unused-argument
        """Method to process websocket messages."""
        global_value.ssl_Mutual_exclusion = True
        logger = logging.getLogger(__name__)
        logger.debug(message)

        message = json.loads(str(message))


        technical_indicators(self.api, message, self.api_dict_clean)
        time_sync(self.api, message)
        heartbeat(self.api, message)
        balances(self.api, message)
        profile(self.api, message)
        balance_changed(self.api, message)
        candles(self.api, message)
        buy_complete(self.api, message)
        option(self.api, message)
        position_history(self.api, message)
        list_info_data(self.api, message)
        candle_generated_realtime(self.api, message, self.dict_queue_add)
        candle_generated_v2(self.api, message, self.dict_queue_add)
        commission_changed(self.api, message)
        socket_option_opened(self.api, message)
        api_option_init_all_result(self.api, message)
        initialization_data(self.api, message)
        underlying_list(self.api, message)
        instruments(self.api, message)
        financial_information(self.api, message)
        position_changed(self.api, message)
        option_opened(self.api, message)
        option_closed(self.api, message)
        top_assets_updated(self.api, message)
        strike_list(self.api, message)
        api_game_betinfo_result(self.api, message)
        traders_mood_changed(self.api, message)
         # ------for forex&cfd&crypto..
        order_placed_temp(self.api, message)
        order(self.api, message)
        position(self.api, message)
        positions(self.api, message)
        order_placed_temp(self.api, message)
        deferred_orders(self.api, message)
        history_positions(self.api, message)
        available_leverages(self.api, message)
        order_canceled(self.api, message)
        position_closed(self.api, message)
        overnight_fee(self.api, message)
        api_game_getoptions_result(self.api, message)
        sold_options(self.api, message)
        tpsl_changed(self.api, message)
        auto_margin_call_changed(self.api, message)
        digital_option_placed(self.api, message, self.api_dict_clean)
        result(self.api, message)
        instrument_quotes_generated(self.api, message)
        training_balance_reset(self.api, message)
        socket_option_closed(self.api, message)
        live_deal_binary_option_placed(self.api, message)
        live_deal_digital_option(self.api, message)
        leaderboard_deals_client(self.api, message)
        live_deal(self.api, message)
        user_profile_client(self.api, message)
        leaderboard_userinfo_deals_client(self.api, message)
        users_availability(self.api, message)
        client_price_generated(self.api, message)

        global_value.ssl_Mutual_exclusion = False

    def on_error(wss, _, error):  # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)
        global_value.websocket_error_reason = str(error)
        global_value.check_websocket_if_error = True

    def on_open(wss, _):  # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        global_value.check_websocket_if_connect = 1

    def on_close(wss, _):  # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect = 0
