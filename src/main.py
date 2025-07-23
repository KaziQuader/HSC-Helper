from prepare_data import create_vector_db

def main():
    create_vector_db('data/HSC26-Bangla1st-Paper.pdf', 'clean/full_text.txt')

if __name__ == "__main__":
    main()