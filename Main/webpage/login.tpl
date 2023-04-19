<!DOCTYPE html>
<html lang="en">

<head>
    <title>Network Penetration Testing Tool</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</head>

<body>
    <!-- Start -->
    <div class="container mt-5">
        <div class="text-center">
            <p>
                <h1>Login</h1>
            </p>

        </div>
        <section class="h-100">
            <div class="container h-100">
                <div class="row justify-content-sm-center h-100">
                    <div class="col-xxl-4 col-xl-5 col-lg-5 col-md-7 col-sm-9">
                        <div class="card shadow-lg">
                            <div class="card-body p-5 text-center">
                                <form method="POST" class="needs-validation" novalidate="" autocomplete="off">
                                    <div class="mb-3">
                                        <div class="form-floating">
                                            <input type="text" class="form-control" id="username" name="username" placeholder="Username">
                                            <label for="floatingInput">Username</label>
                                        </div>
                                    </div>
                            
                                    <div class="mb-3">
                                        <div class="form-floating">
                                            <input type="password" class="form-control" id="password" name="password" placeholder="Password">
                                            <label for="floatingPassword">Password</label>
                                        </div>
                                        <br>
                                        <div class="text-center">
                                            <button type="submit" id="login" name="login" class="btn btn-outline-primary">Login</button>
                                        </div>
                                    </div>
                                </form>
                                % if login_status:
                                    <div class="alert alert-danger" role="alert">
                                        {{login_status}}
                                    </div>
                                % end
                            </div>                            
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</body>


</html>