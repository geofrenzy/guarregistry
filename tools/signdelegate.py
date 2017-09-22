import docker


def sign_zone(zonename):
    client = docker.from_env()

    for container in client.containers.list(zonename):
        if container.attrs["Name"] == "/gf-guar-pdns-registry":
            signstring = "pdnsutil secure-zone " + zonename
            signresponse = container.exec_run(signstring).splitlines()
            for line in signresponse:
                print(line.decode())
            rectifystring = "pdnsutil rectify-zone " + zonename
            rectifyresponse = container.exec_run(rectifystring).splitlines()
            for line in rectifyresponse:
                print(line.decode())
            print("\n\n\n")
            print("!" * 80)
            print("PLEASE PROVIDE THE FOLLOWING INFORMATION TO THE UAS ROOT ADMINISTRATOR")
            print("*" * 80)
            showstring = "pdnsutil show-zone " + zonename
            showresponse = container.exec_run(showstring).splitlines()
            for line in showresponse:
                print(line.decode())
            print("*" * 80)


if __name__ == "__main__":
    domainname = input("enter domain name: ")
    sign_zone(domainname)
