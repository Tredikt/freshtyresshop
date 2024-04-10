function endOrder() {
    let form = document.createElement("form")
    form.method = "POST"

    document.body.append(form)
    form.submit()
}