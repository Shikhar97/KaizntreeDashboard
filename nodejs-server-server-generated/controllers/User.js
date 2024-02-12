'use strict';

var utils = require('../utils/writer.js');
var User = require('../service/UserService');

module.exports.apiV1AuthLoginPOST = function apiV1AuthLoginPOST (req, res, next, body) {
  User.apiV1AuthLoginPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1AuthLogoutGET = function apiV1AuthLogoutGET (req, res, next) {
  User.apiV1AuthLogoutGET()
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1AuthRegisterPOST = function apiV1AuthRegisterPOST (req, res, next, body) {
  User.apiV1AuthRegisterPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1AuthReset_passwordConfirmPATCH = function apiV1AuthReset_passwordConfirmPATCH (req, res, next, body) {
  User.apiV1AuthReset_passwordConfirmPATCH(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1AuthReset_passwordPOST = function apiV1AuthReset_passwordPOST (req, res, next, body) {
  User.apiV1AuthReset_passwordPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.apiV1AuthReset_password_confirmUidb64TokenGET = function apiV1AuthReset_password_confirmUidb64TokenGET (req, res, next, uidb64, token) {
  User.apiV1AuthReset_password_confirmUidb64TokenGET(uidb64, token)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
