const API = new class {
    async get(url) {
        return await fetch(url).then((response) => response.json())
    }

    async put(url, data = {}) {
        return await fetch(url, {
            method: 'PUT',
            body: JSON.stringify(data),
        }).then((response) => response.json())
    }

    async upload(url, files) {
        const data = new FormData()
        files.map((file) => data.append('files', file))

        return await fetch(url, {
            method: 'POST',
            body: data,
        }).then((response) => response.json())
    }
}

export default API

