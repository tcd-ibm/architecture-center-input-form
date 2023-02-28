class User {
    constructor(accessToken) {
        this.accessToken = accessToken;
    }

    isAdmin() {
        return true;
    }
}

export default User;