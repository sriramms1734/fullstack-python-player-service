export default async function fetchData(input, limit=10, offset=10) {
    const endpoint = input ? `/v1/players/${input}?limit=${limit}&offset=${offset}`: `/v1/players?limit=${limit}&offset=${offset}`;
    return fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            return data;
        }).catch(error => {
            console.log('oops there was an error', error)
    })
};