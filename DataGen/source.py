from Configuration.Config.DataGenConfig import DataGenConfig
from DataGen.Crypt import CombineCrypt
from DataGen.Datasets import Datasets
from DataGen.Key import Key
from DataGen.Save import Save, File


def encryption_decryption_pipeline(dataset, key_group, additional_message):
    # Messages encryption
    encrypted_messages, encrypted_index = CombineCrypt.crypt_key_message_group(
        key_group,
        dataset,
        additional_message=additional_message
    )

    # Messages decryption
    decrypted_messages, decrypted_index = CombineCrypt.decrypt_key_message_group(
        encrypted_messages,
        encrypted_index,
        additional_message=additional_message
    )

    # Success check
    CombineCrypt.crypt_decrypt_success_check(
        encrypted_index,
        decrypted_index,
        additional_message=additional_message
    )

    # Caching results
    File.index_to_file(
        encrypted_index,
        DataGenConfig.cipher_generated_dataset_root_path,
        DataGenConfig.reference_bit_index,
        Save.Save.Bit,
        additional_message=additional_message
    )


def main():
    # Dataset
    dataset = Datasets.read_pan(DataGenConfig.plaintext_dataset_root_path)

    # Keys generation
    keys_group_zero, keys_group_one = Key.generate_zero_one_groups(
        reference_bit_index=DataGenConfig.reference_bit_index,
        wanted_key_group_size=DataGenConfig.wanted_key_group_size
    )

    # Pipeline invocation
    encryption_decryption_pipeline(
        dataset,
        keys_group_zero,
        'Zero key group'
    )

    encryption_decryption_pipeline(
        dataset,
        keys_group_one,
        'One key group'
    )


if __name__ == '__main__':
    main()
