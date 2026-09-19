import Foundation
import FoundationModels

private struct ModelInfo: Encodable {
    let status: String
    let reason: String?
    let model_variant: String?
}

@_cdecl("getFoundationModelsInfo")
public func getFoundationModelsInfo() -> UnsafeMutablePointer<CChar>? {
    let model = SystemLanguageModel.default
    let info: ModelInfo
    switch model.availability {
    case .available:
        let variant: String?
        if #available(macOS 27.0, *) {
            variant = model.variant.displayName
        } else {
            variant = nil
        }
        info = ModelInfo(status: "available", reason: nil, model_variant: variant)
    case .unavailable(let reason):
        let name: String
        switch reason {
        case .deviceNotEligible:
            name = "deviceNotEligible"
        case .appleIntelligenceNotEnabled:
            name = "appleIntelligenceNotEnabled"
        case .modelNotReady:
            name = "modelNotReady"
        @unknown default:
            name = "unknown"
        }
        info = ModelInfo(status: "unavailable", reason: name, model_variant: nil)
    }
    guard let data = try? JSONEncoder().encode(info),
          let json = String(data: data, encoding: .utf8) else {
        return nil
    }
    return strdup(json)
}

@_cdecl("freeFoundationModelsInfo")
public func freeFoundationModelsInfo(_ pointer: UnsafeMutablePointer<CChar>?) {
    free(pointer)
}
