from pengelola_basisdata import PengelolaBasisdata


def main():

    pengelola_basisdata = PengelolaBasisdata()

    data_sekarang = pengelola_basisdata.get_status_sekarang()
    print(data_sekarang)

    jumlah = pengelola_basisdata.jumlah_data()
    print("jumlah :",jumlah[0][0])

# ============================================================================
if __name__ == "__main__":
    print("Mulai .")
    main()
