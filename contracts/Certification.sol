// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Certification {
    struct Certificate {
        string uid;
        string candidate_name;
        string course_name;
        string notes;
        string grad;
        string org_name;
        string ipfs_hash;
        string birthday;
    }

    mapping(string => Certificate) public certificates;
    event certificateGenerated(string certificate_id);

    function generateCertificate(
        string memory _certificate_id,
        string memory _uid,
        string memory _candidate_name,
        string memory _course_name,
        string memory _notes,
        string memory _grad,
        string memory _org_name,
        string memory _birthday,
        string memory _ipfs_hash
    ) public {
        // Check if certificate with the given ID already exists
        require(
            bytes(certificates[_certificate_id].ipfs_hash).length == 0,
            "Certificate with this ID already exists"
        );

        // Create the certificate
        Certificate memory cert = Certificate({
            uid: _uid,
            candidate_name: _candidate_name,
            course_name: _course_name,
            notes: _notes,
            grad: _grad,
            org_name: _org_name,
            birthday: _birthday,
            ipfs_hash: _ipfs_hash
        });

        // Store the certificate in the mapping
        certificates[_certificate_id] = cert;

        // Emit an event
        emit certificateGenerated(_certificate_id);
    }

    function getCertificate(
        string memory _certificate_id
    )
        public
        view
        returns (
            string memory _uid,
            string memory _candidate_name,
            string memory _course_name,
            string memory _notes,
            string memory _grad,
            string memory _org_name,
            string memory _birthday,
            string memory _ipfs_hash
        )
    {
        Certificate memory cert = certificates[_certificate_id];

        // Check if the certificate with the given ID exists
        require(
            bytes(certificates[_certificate_id].ipfs_hash).length != 0,
            "Certificate with this ID does not exist"
        );

        // Return the values from the certificate
        return (
            cert.uid,
            cert.candidate_name,
            cert.course_name,
            cert.notes,
            cert.grad,
            cert.org_name,
            cert.birthday,
            cert.ipfs_hash
        );
    }

    function isVerified(string memory _certificate_id, string memory _uid) public view returns (bool) {
    Certificate memory cert = certificates[_certificate_id];
    require(bytes(cert.ipfs_hash).length > 0, "Certificate does not exist");
    
    // Compare UID from certificate with uploaded UID
    require(keccak256(abi.encodePacked(cert.uid)) == keccak256(abi.encodePacked(_uid)), "UID mismatch");
    
    // Add more checks as needed (e.g., compare course_name, org_name, etc.)
    
    return true;
    }



}
