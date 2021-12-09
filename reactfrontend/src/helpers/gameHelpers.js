export default function processGamesData(data) {
    let resp = []
    for (let d in data) {
        let r = {}
        r["id"] = d.uid
        r["title"] = d.title
        r["starting_balance"] = d.starting_balance
        r["rules"] = d.rules
        r["portfolios"] = d.portfolios
        resp.push(r)
    }
    console.log(resp)
    return resp

}
