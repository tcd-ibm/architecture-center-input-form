class User {
    constructor(accessToken, tokenExpirationDate, role) {
        this.accessToken = accessToken;
        this.tokenExpirationDate = tokenExpirationDate;
        this.role = role;
    }

    isExpired() {
        return new Date() > this.tokenExpirationDate;
    }

    isAdmin() {
        return this.role !== 0;
    }
}

export default User;