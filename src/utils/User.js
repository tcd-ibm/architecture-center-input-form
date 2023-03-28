class User {
    constructor(accessToken, role) {
        this.accessToken = accessToken;
        this.role = role;
    }

    isAdmin() {
        return isAdminRole(this.role);
    }
}

export function isAdminRole(role) {
    return role !== 0;
}

export default User;