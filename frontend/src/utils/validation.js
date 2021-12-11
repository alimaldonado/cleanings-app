/**
 * VERY simple email validation
 *
 * @param {String} text - email to be validated
 * @return {Boolean}
 *
 */
export function validateEmail(text) {
  return text?.indexOf("@") !== -1;
}

/**
 * Ensures password is at least a certain lenght
 *
 * @param {String} password - password to be validated
 * @param {Integer} length - length password must be as long as
 * @return {Boolean}
 */
export function validatePassword(password, length = 7) {
  return password?.length >= length;
}

/**
 * Ensures an username consists of only letters, numbers, underscores and dashes
 *
 * @param {String} username - username to be validated
 * @return {Boolean}
 */
export function validateUsername(username) {
  // I'm gonna believe you on this
  return /^[a-zA-Z0-9_-]+$/.test(username);
}

// eslint-disable-next-line
export default {
  email: validateEmail,
  password: validatePassword,
  username: validateUsername,
};
