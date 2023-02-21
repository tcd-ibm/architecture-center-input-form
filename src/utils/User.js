class User {
    constructor(accessToken) {
        this.accessToken = accessToken;
    }

    isAdmin() {
        return false;
    }
}

export default User;