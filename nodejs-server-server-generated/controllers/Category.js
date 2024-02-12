'use strict';

var utils = require('../utils/writer.js');
var Category = require('../service/CategoryService');

module.exports.apiV1ItemsCategoryAddPOST = function apiV1ItemsCategoryAddPOST (req, res, next, body) {
  Category.apiV1ItemsCategoryAddPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1ItemsCategoryDeleteCategory_nameDELETE = function apiV1ItemsCategoryDeleteCategory_nameDELETE (req, res, next, category_name) {
  Category.apiV1ItemsCategoryDeleteCategory_nameDELETE(category_name)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
