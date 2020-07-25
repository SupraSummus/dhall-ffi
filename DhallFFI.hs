{-# LANGUAGE StandaloneDeriving #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}

module DhallFFI where

import Data.Text as T
import Dhall.Core
import Dhall.Src
import Foreign.C.String
import Foreign.StablePtr
import Foreign.Ptr
import Foreign.Storable
import qualified Dhall.Parser
import Data.Data
import Dhall.Crypto
import Data.Bifunctor
import GHC.Generics
import Data.Binary
import qualified Data.ByteString.Lazy as B
import Foreign.Marshal.Array

-- there may be a good reason why these classes are not defined in dhall package
deriving instance Data Directory
deriving instance Data File
deriving instance Data FilePrefix
deriving instance Data Import
deriving instance Data ImportHashed
deriving instance Data ImportMode
deriving instance Data ImportType
deriving instance Data Scheme
deriving instance Data SHA256Digest
deriving instance Data URL

type FFIExpr = Expr Src Import

stableNull :: StablePtr a
stableNull = castPtrToStablePtr nullPtr

foreign export ccall exprFromText :: CString -> IO (StablePtr FFIExpr)
exprFromText code_ = do
  code <- peekCString code_
  case Dhall.Parser.exprFromText "<toplevel>" (T.pack code) of
    Right expr -> newStablePtr $ expr
    Left err -> return stableNull

getConstr :: Data a => StablePtr a -> IO Int
getConstr ptr = do
  v <- deRefStablePtr ptr
  return $ constrIndex $ toConstr v

getData :: Data a => StablePtr a -> Int -> IO (Ptr ())
getData ptr i = do
  v <- deRefStablePtr ptr
  gmapQi i (fmap castStablePtrToPtr . newStablePtr) v

constrRepToInt :: ConstrRep -> Int
constrRepToInt (AlgConstr i) = i
constrRepToInt (IntConstr i) = fromIntegral i

getDirect :: Data a => StablePtr a -> Int -> IO Int
getDirect ptr i = do
  v <- deRefStablePtr ptr
  return $ constrRepToInt $ constrRep $ gmapQi i toConstr v

-- ### generic ###

foreign export ccall unlink :: StablePtr a -> IO ()
unlink = freeStablePtr

-- ### expr ###

foreign export ccall exprGetConstr :: StablePtr (Expr Src Import) -> IO Int
exprGetConstr = getConstr

foreign export ccall exprGetData :: StablePtr (Expr Src Import) -> Int -> IO (Ptr ())
exprGetData = getData

foreign export ccall exprGetDirect :: StablePtr (Expr Src Import) -> Int -> IO Int
exprGetDirect = getDirect

-- ### var ###

foreign export ccall varGetData :: StablePtr Var -> Int -> IO (Ptr ())
varGetData = getData

foreign export ccall varGetDirect :: StablePtr Var -> Int -> IO Int
varGetDirect = getDirect

-- ### text ###

foreign export ccall textToByteString :: StablePtr Text -> IO (StablePtr B.ByteString)
textToByteString ptr = do
  t <- deRefStablePtr ptr
  newStablePtr $ encode t

foreign export ccall byteStringSize :: StablePtr B.ByteString -> IO Int
byteStringSize ptr = do
  b <- deRefStablePtr ptr
  return $ fromIntegral $ B.length b

foreign export ccall byteStringWrite :: StablePtr B.ByteString -> Ptr Word8 -> IO ()
byteStringWrite ptr dst = do
  b <- deRefStablePtr ptr
  pokeArray dst (B.unpack b)
