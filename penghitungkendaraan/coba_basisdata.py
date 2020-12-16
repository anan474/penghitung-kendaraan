from pengelola_basisdata import PengelolaBasisdata


def main():

    pengelola_basisdata = PengelolaBasisdata()
    # pengelola_basisdata.get_data_hari_ini()
    pengelola_basisdata.get_status_sekarang()
    pengelola_basisdata.jumlah_data()


# ============================================================================
if __name__ == "__main__":
    print("Mulai .")
    main()
