#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, g, request, jsonify)

from application.config import base_config, production_config
from application.utils import (write_command_sql, load_status_sql, get_colors, convert_rgb_to_hex,
                               get_color_hex, get_modes, make_mode_color_list_dict, make_custom_color_dict)
from application import __version__
from application.template_filters import template_filters


def create_app(config=None):
    app = Flask(import_name=__name__)
    app.config.from_object(base_config)

    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(production_config)

    for template_filter in template_filters:
        app.add_template_filter(template_filter)

    @app.before_request
    def before_request():
        if 'static' not in request.path:
            g.status = load_status_sql()
            app.config['COLORS'] = get_colors()
            app.config['MODES'] = get_modes()
            if request.path == '/mode-creator/':
                app.config['CUSTOM_MODES'] = make_mode_color_list_dict()
            if request.path == '/color-creator/':
                app.config['CUSTOM_COLORS'], app.config['CUSTOM_HEXES'] = make_custom_color_dict()
            if g.status.get('program') == app.config['PROGRAM']['Color']:
                led_colors = g.status['lights']
                # add the hex code if we're in demo mode and on the main page...
                # we check the main page to keep this from showing up on the mode creator
                if request.path == '/':
                    if len(led_colors[0]) > 5 and app.config['COLORS'].get(led_colors[0]) is None:
                        app.config['COLORS'].update({led_colors[0]: led_colors[0]})
                # if all colors match set matching flag
                if led_colors[0] == led_colors[1] == led_colors[2]:
                    g.status.update({'leds_match': True})
                    g.status.update({'led_color': led_colors[0]})
                else:
                    g.status.update({'leds_match': False})
                    g.status.update({'led_color': -1})
            else:
                g.status.update({'leds_match': False})

    @app.route('/version/', methods=['GET'])
    def version():
        return __version__

    @app.after_request
    def add_header(response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response

    ############################################################################
    # HOMEPAGE ROUTES
    ############################################################################
    @app.route('/', methods=['GET'])
    def homepage():
        app.logger.debug('rendering homepage')
        return render_template('homepage/homepage.html')

    @app.route('/change-power/', methods=['POST'])
    def change_power():
        if int(request.form['power']) == 0:
            power = False
        else:
            power = True
        write_command_sql(power=power)
        return jsonify({}, 200, {})

    @app.route('/change-leds/', methods=['POST'])
    def change_leds():
        led_1 = int(request.form['led_1'])
        led_2 = int(request.form['led_2'])
        led_3 = int(request.form['led_3'])
        write_command_sql(colors=[led_1, led_2, led_3])
        return jsonify({}, 200, {})

    @app.route('/change-mode/', methods=['POST'])
    def change_mode():
        mode = int(request.form['mode'])
        write_command_sql(mode=mode)
        return jsonify({}, 200, {})

    @app.route('/change-brightness/', methods=['POST'])
    def change_brightness():
        brightness = float(request.form['brightness'])
        write_command_sql(bright=brightness)
        return jsonify({}, 200, {})

    @app.route('/change-delay/', methods=['POST'])
    def change_delay():
        delay = float(request.form['delay'])
        write_command_sql(delay=delay)
        return jsonify({}, 200, {})

    @app.route('/change-shifter/', methods=['POST'])
    def change_shifter():
        shifter = int(request.form['shifter'])
        write_command_sql(shifter=shifter)
        return jsonify({}, 200, {})

    @app.route('/change-sync/', methods=['POST'])
    def change_sync():
        sync = int(request.form['sync'])
        write_command_sql(sync=sync)
        return jsonify({}, 200, {})

    @app.route('/get-status/', methods=['GET'])
    def get_status():
        try:
            return jsonify({}, 200, {})
        except Exception as e:
            app.logger.exception(e)
            return jsonify({'message': [app.config['GENERIC_FORM_ERROR_MESSAGE']]}), 500, {}

    ############################################################################
    # COLOR CREATOR ROUTES
    ############################################################################

    @app.route('/color-creator/', methods=['GET'])
    def color_creator():
        return render_template('color_creator/color_creator.html')

    @app.route('/demo-color/', methods=['POST'])
    def demo_color():
        red = int(request.form['red'])
        green = int(request.form['green'])
        blue = int(request.form['blue'])
        hex = convert_rgb_to_hex(red, green, blue)
        write_command_sql(color=hex)
        return jsonify({}, 200, {})

    @app.route('/save-color/', methods=['POST'])
    def save_color():
        red = int(request.form['red'])
        green = int(request.form['green'])
        blue = int(request.form['blue'])
        name = request.form['name']
        hex = convert_rgb_to_hex(red, green, blue)
        write_command_sql(save=[hex, name])
        return jsonify({}, 200, {})

    @app.route('/delete-color/', methods=['POST'])
    def delete_color():
        color_id = int(request.form['color_id'])
        # print('got our id boy', color_id)
        hex = get_color_hex(color_id)
        # print('got our hex boy: {}'.format(hex))
        write_command_sql(delete=hex)
        return jsonify({}, 200, {})
    ############################################################################
    # MODE CREATOR ROUTES
    ############################################################################

    @app.route('/mode-creator/', methods=['GET'])
    def mode_creator():
        return render_template('mode_creator/mode_creator.html')

    @app.route('/save-mode/', methods=['POST'])
    def save_mode():
        color_list = request.form['colors']
        name = request.form['name']
        write_command_sql(addmode=[name, color_list])
        return jsonify({}, 200, {})

    @app.route('/delete-mode/', methods=['POST'])
    def delete_mode():
        mode_id = int(request.form['mode_id'])
        write_command_sql(deletemode=mode_id)
        return jsonify({}, 200, {})

    ############################################################################
    # TIMER SETTINGS ROUTES
    ############################################################################

    @app.route('/timer/', methods=['GET'])
    def timer_settings():
        return render_template('timer_settings/timer_settings.html')

    @app.route('/timer/change-times/', methods=['POST'])
    def change_times():
        ontime = request.form['ontime']
        offtime = request.form['offtime']
        write_command_sql(ontime=ontime, offtime=offtime)
        return jsonify({}, 200, {})

    @app.route('/timer/power/', methods=['POST'])
    def change_timer_power():
        if request.form['power'].lower() == 'true':
            write_command_sql(timerset=1)
        else:
            write_command_sql(timerset=0)
        return jsonify({}, 200, {})

    return app


if __name__ == "__main__":
    from application.config import instance_config

    app = create_app(instance_config)
    app.run(port=5000)
