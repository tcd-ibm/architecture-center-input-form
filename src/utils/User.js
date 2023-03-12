class User {
    constructor(accessToken, role) {
        this.accessToken = accessToken;
        this.role = role;
    }

    isAdmin() {
        return this.role !== 0;
    }
}

export default User;