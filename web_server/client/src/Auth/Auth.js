// authenticate user through token, store token in local storage
// check whether user is authenticated (token existed in local storage) for the router

class Auth {
    static authenticateUser(token, email) {
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
    }

    static isUserAuthenticated() {
        return localStorage.getItem('token') != null;
    }

    static deauthenticateUser() {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    }

    static getToken() {
        return localStorage.getItem('token');
    }

    static getEmail() {
        return localStorage.getItem('email');
    }
}

export default Auth;