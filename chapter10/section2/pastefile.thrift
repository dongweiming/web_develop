struct PasteFile {
    1: required i32 id,
    2: required string filename,
    3: required string filehash,
    4: required string filemd5,
    5: required string uploadtime,
    6: required string mimetype,
    7: required i64 size,
    8: required string url_s,
    9: required string url_i,
    10: required list<i32> image_size,
    11: required string url_d,
    12: required string url_p,
    13: required string size_humanize,
    14: required string type,
    15: required string quoteurl,
}

struct CreatePasteFileRequest {
    1: required string filehash,
    2: required string filename,
    3: required string mimetype,
    4: optional i32 width,
    5: optional i32 height,
}

exception ImageNotSupported {
    1: string message
}

exception UploadImageError {
    1: string message
}

exception NotFound {
    1: i32 code
}

exception ServiceUnavailable {
    1: string message
}

service PasteFileService {
    PasteFile get(1:i32 pid)
        throws(
            1: ServiceUnavailable service_error,
            2: NotFound not_found
        ),
    list<string> get_file_info(1:string filename, 2:string mimetype)
    PasteFile create(1: CreatePasteFileRequest request)
        throws(
            1: ServiceUnavailable service_error,
            2: ImageNotSupported error,
            3: UploadImageError image_error
        ),
}
