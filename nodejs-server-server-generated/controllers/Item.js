'use strict';

var utils = require('../utils/writer.js');
var Item = require('../service/ItemService');

module.exports.apiV1ItemsAddPOST = function apiV1ItemsAddPOST (req, res, next, body) {
  Item.apiV1ItemsAddPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1ItemsDeleteStock_idDELETE = function apiV1ItemsDeleteStock_idDELETE (req, res, next, stock_id) {
  Item.apiV1ItemsDeleteStock_idDELETE(stock_id)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1ItemsListGET = function apiV1ItemsListGET (req, res, next, created_after, created_before, status, category) {
  Item.apiV1ItemsListGET(created_after, created_before, status, category)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
