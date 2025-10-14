-- post_body.lua
wrk.method = "POST"
wrk.body = "{}" -- Пустой JSON-объект, чтобы имитировать корректный POST-запрос
wrk.headers["Content-Type"] = "application/json"