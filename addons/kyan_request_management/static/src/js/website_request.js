/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";


publicWidget.registry.SendRequestMenu = publicWidget.Widget.extend({
    selector: '.send_data_request',
    events: {
        'click .sendRequestclick': '_onClickCreate',
        'change .onchangerequesttype': '_onchangerequesttype',
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
        this._onchangerequesttype();
    },

    //  create_request_page website
    
    _onClickCreate: async function (ev) {
        // ev.preventDefault();
        var msg_form = $('form[name=create_request_page]');
        var request_info = msg_form.serializeArray();
        var msg_error = $("#request_error");
        var msg_success = $("#message_success");

        var sendRequestPromise = this.rpc(
            `/new/request_type`,
            {
                'data': request_info,
            }
        ).then(function (result) {
            if (result.msg) {
                msg_error.removeClass('d-none');
                msg_error.html(result.msg);
            }
            if (result === true){
                $('#mywebsiterequest').modal('hide');
            }
            return result
        });

        Promise.all([sendRequestPromise])
    },

    // Hide and Show (Amount, Startdate, Enddate)

    _onchangerequesttype: function (event) {
        $('#amount_field').hide();
        $('#start_date').hide();
        $('#start_date_lable').hide();
        $('#end_date').hide();
        $('#end_date_lable').hide();

        var quantity = parseInt($('#request_selection').val());

        var HideShowPromise = this.rpc(
            `/refrence2/product/`,
            {
                'product': quantity,
            }
        ).then(function (result) {
            if (result === '') {
                $('#amount_field').hide();
                $('#start_date').hide();
                $('#start_date_lable').hide();
                $('#end_date').hide();
                $('#end_date_lable').hide();
            } else if (result === 'loan' || result === 'advance_salary') {
                $('#amount_field').show();
                $('#start_date').hide();
                $('#start_date_lable').hide();
                $('#end_date').hide();
                $('#end_date_lable').hide();
            } else if (result === 'leave') {
                $('#start_date').show();
                $('#start_date_lable').show();
                $('#end_date').show();
                $('#end_date_lable').show();
            } else {
                $('#amount_field').hide();
                $('#start_date').hide();
                $('#start_date_lable').hide();
                $('#end_date').hide();
                $('#end_date_lable').hide();
            }
        });

        Promise.all([HideShowPromise])

    },
});

export default publicWidget.registry.SendRequestMenu;
